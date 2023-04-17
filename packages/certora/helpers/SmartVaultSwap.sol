// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC20/IERC20.sol';
import '@mimic-fi/v2-helpers/contracts/math/FixedPoint.sol';
import '@openzeppelin/contracts/utils/Address.sol';
import '@openzeppelin/contracts/utils/math/Math.sol';
import '@mimic-fi/v2-helpers/contracts/utils/Denominations.sol';
import '@mimic-fi/v2-helpers/contracts/math/UncheckedMath.sol';
import '@mimic-fi/v2-helpers/contracts/auth/Authorizer.sol';
interface IPriceOracle {
    /*
     * @param provider Contract providing the price feeds to use by the oracle
     * @param base Token to rate
     * @param quote Token used for the price rate
     */
    function getPrice(address provider, address base, address quote) external view returns (uint256);
}
interface ISmartVaultSwap {

    enum SwapLimit {
        Slippage,
        MinAmountOut
    }

    function wrappedNativeToken() external view returns (address);

    function feeCollector() external view returns (address);
    
    function getPrice(address base, address quote) external view returns (uint256);
    
    function swap(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        SwapLimit limitType,
        uint256 limitAmount,
        bytes memory data
    ) external returns (uint256 amountOut);

    function withdraw(address token, uint256 amount, address recipient, bytes memory data) external returns(uint256 withdrawn);
        
}

contract SmartVault is ISmartVaultSwap, Authorizer {
    using FixedPoint for uint256;
    using UncheckedMath for uint256;

    /**
     * @dev Fee configuration parameters
     * @param pct Percentage expressed using 16 decimals (1e18 = 100%)
     * @param cap Maximum amount of fees to be charged per period
     * @param token Address of the token to express the cap amount
     * @param period Period length in seconds
     * @param totalCharged Total amount of fees charged in the current period
     * @param nextResetTime Current cap period end date
     */
    struct Fee {
        uint256 pct;
        uint256 cap;
        address token;
        uint256 period;
        uint256 totalCharged;
        uint256 nextResetTime;
    }
    
    address public immutable override wrappedNativeToken;
    address public priceOracle;
    // Fee collector address where fees will be deposited
    address public override feeCollector;
    // Swap fee configuration
    Fee public swapFee;
    // an address to represent the dex that is exchanging token with the smart vault 
    address public dex;
    // AMM swapper (price -> amount -> block.timestamp)
    mapping(uint256 => mapping(uint256 => mapping(uint256 => uint256))) DexSwap;

    constructor(address _wrappedNativeToken){
        wrappedNativeToken = _wrappedNativeToken;
    }

    /**
     * @dev Tells the price of a token (base) in a given quote
     * @param base Token to rate
     * @param quote Token used for the price rate
     */
    function getPrice(address base, address quote) public view override returns (uint256) {
        return IPriceOracle(priceOracle).getPrice(address(this), base, quote);
    }

    function setPriceFeed(address base, address quote, address feed)
        public
        auth {}

    function swap(
        uint8,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        SwapLimit limitType,
        uint256 limitAmount,
        bytes memory
    ) external override auth returns (uint256 amountOut) {
        require(tokenIn != tokenOut, 'SWAP_SAME_TOKEN');
        //require(swapConnector != address(0), 'SWAP_CONNECTOR_NOT_SET');

        uint256 minAmountOut;
        uint256 price = getPrice(tokenIn, tokenOut);
        if (limitType == SwapLimit.MinAmountOut) {
            minAmountOut = limitAmount;
        } else if (limitType == SwapLimit.Slippage) {
            require(limitAmount <= FixedPoint.ONE, 'SWAP_SLIPPAGE_ABOVE_ONE');
            // No need for checked math as we are checking it manually beforehand
            // Always round up the expected min amount out. Limit amount is slippage.
            minAmountOut = amountIn * price * (FixedPoint.ONE - limitAmount);
            // minAmountOut = amountIn.mulUp(price).mulUp(FixedPoint.ONE.uncheckedSub(limitAmount));
        } else {
            revert('SWAP_INVALID_LIMIT_TYPE');
        }

        uint256 preBalanceIn = IERC20(tokenIn).balanceOf(address(this));
        uint256 preBalanceOut = IERC20(tokenOut).balanceOf(address(this));
        _swap(price, tokenIn, tokenOut, amountIn);
        //swapConnector.swap(source, tokenIn, tokenOut, amountIn, minAmountOut, data);

        uint256 postBalanceIn = IERC20(tokenIn).balanceOf(address(this));
        require(postBalanceIn >= preBalanceIn - amountIn, 'SWAP_BAD_TOKEN_IN_BALANCE');

        uint256 amountOutBeforeFees = IERC20(tokenOut).balanceOf(address(this)) - preBalanceOut;
        require(amountOutBeforeFees >= minAmountOut, 'SWAP_MIN_AMOUNT');

        uint256 swapFeeAmount = _payFee(tokenOut, amountOutBeforeFees, swapFee);
        amountOut = amountOutBeforeFees - swapFeeAmount;
        // emit Swap(source, tokenIn, tokenOut, amountIn, amountOut, minAmountOut, swapFeeAmount, data);
    }

    function _swap(uint256 price, address tokenIn, address tokenOut, uint256 amountIn) internal {
        uint256 amountOut = DexSwap[price][amountIn][block.timestamp];
        _safeTransferFrom(tokenIn, dex, address(this), amountIn);
        _safeTransfer(tokenOut, dex, amountOut);
    }

    /**
     * @dev Internal function to pay the amount of fees to be charged based on a fee configuration to the fee collector
     * @param token Token being charged
     * @param amount Token amount to be taxed with fees
     * @param fee Fee configuration to be applied
     * @return paidAmount Amount of fees paid to the fee collector
     */
    function _payFee(address token, uint256 amount, Fee storage fee) internal returns (uint256 paidAmount) {
        // Fee amounts are always rounded down
        uint256 feeAmount = amount.mulDown(fee.pct);

        // If cap amount or cap period are not set, charge the entire amount
        if (fee.token == address(0) || fee.cap == 0 || fee.period == 0) {
            _safeTransfer(token, feeCollector, feeAmount);
            return feeAmount;
        }

        // Reset cap totalizator if necessary
        if (block.timestamp >= fee.nextResetTime) {
            fee.totalCharged = 0;
            fee.nextResetTime = block.timestamp + fee.period;
        }

        // Calc fee amount in the fee token used for the cap
        uint256 feeTokenPrice = getPrice(token, fee.token);
        uint256 feeAmountInFeeToken = feeAmount.mulDown(feeTokenPrice);

        // Compute fee amount picking the minimum between the chargeable amount and the remaining part for the cap
        if (fee.totalCharged + feeAmountInFeeToken <= fee.cap) {
            paidAmount = feeAmount;
            fee.totalCharged += feeAmountInFeeToken;
        } else if (fee.totalCharged < fee.cap) {
            paidAmount = (fee.cap.uncheckedSub(fee.totalCharged) * feeAmount) / feeAmountInFeeToken;
            fee.totalCharged = fee.cap;
        } else {
            // This case is when the total charged amount is already greater than the cap amount. It could happen if
            // the cap amounts is decreased or if the cap token is changed. In this case the total charged amount is
            // not updated, and the amount to paid is zero.
            paidAmount = 0;
        }

        // Pay fee amount to the fee collector
        _safeTransfer(token, feeCollector, paidAmount);
    }

    /**
     * @dev Internal method to transfer ERC20 or native tokens from a Smart Vault
     * @param token Address of the ERC20 token to transfer
     * @param to Address transferring the tokens to
     * @param amount Amount of tokens to transfer
     */
    function _safeTransfer(address token, address to, uint256 amount) internal {
        if (amount == 0) return;
        if (Denominations.isNativeToken(token)) IERC20(wrappedNativeToken).transfer(to, amount);
        else IERC20(token).transfer(to, amount);
    }

    function _safeTransferFrom(address token, address from, address to, uint256 amount) internal {
        if (amount == 0) return;
        if (Denominations.isNativeToken(token)) IERC20(wrappedNativeToken).transferFrom(from, to, amount);
        else IERC20(token).transferFrom(from, to, amount);
    }

    function withdraw(address token, uint256 amount, address recipient, bytes memory)
        external
        override
        auth
        returns (uint256 withdrawn)
    {
        require(amount > 0, 'WITHDRAW_AMOUNT_ZERO');
        require(recipient != address(0), 'RECIPIENT_ZERO');

        uint256 withdrawFeeAmount = 0;
        //uint256 withdrawFeeAmount = recipient == feeCollector ? 0 : _payFee(token, amount, withdrawFee);
        withdrawn = amount - withdrawFeeAmount;
        IERC20(token).transfer(recipient, withdrawn);
    }
}
    