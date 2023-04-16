// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC20/IERC20.sol';

/* symbolic representaiton of a smart vault for verification: 

@mimic-fi/v2-smart-vault/contracts/ISmartVault.sol 

*/

// Using an interface with only the functions we need
interface ISmartVault  {
 
   function getPrice(address base, address quote) external view returns (uint256);

    enum SwapLimit {
        Slippage,
        MinAmountOut
    }
     
    function swap(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        SwapLimit limitType,
        uint256 limitAmount,
        bytes memory data
    ) external returns (uint256 amountOut);


    /**
     * @dev Withdraw tokens to an external account
     * @param token Address of the token to be withdrawn
     * @param amount Amount of tokens to withdraw
     * @param recipient Address where the tokens will be transferred to
     * @param data Extra data that may enable or not different behaviors depending on the implementation
     * @return withdrawn Amount of tokens transferred to the recipient address
     */
    function withdraw(address token, uint256 amount, address recipient, bytes memory data)
        external
        returns (uint256 withdrawn);


     function feeCollector() external view returns (address);    

}

contract SymbolicSmartVault is ISmartVault {

    // price of base to quote per block.timestamp
    // assumption: the price does not change during a block 
    mapping(address => mapping(address => mapping(uint256 => uint256))) symbolicPrice;
    

    address public wrappedNativeToken;

    address public override feeCollector; 

    // an address to represent the dex that is exchanging token with the smart vault 
    address public dex;

    function getPrice(address base, address quote) external override view returns (uint256) {
        return symbolicPrice[base][quote][block.timestamp] ;
    }


    // symbolic representation that the exchange can be not exactly amountIn
    uint256 random;
  
    mapping (uint256 => uint256) symbolicAmounOut;
    mapping (uint256 => mapping(uint256 => uint256)) symbolicMinAmount;
    mapping (address => mapping(uint256 => uint256)) symbolicFeeAmount;
    
    
    

    function swap(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        SwapLimit limitType,
        uint256 limitAmount,
        bytes memory data
    ) external override returns  (uint256 amountOut) {
        require(tokenIn != tokenOut, 'SWAP_SAME_TOKEN');
        
        uint256 minAmountOut;
        if (limitType == SwapLimit.MinAmountOut) {
            minAmountOut = limitAmount;
        } else if (limitType == SwapLimit.Slippage) {

            uint256 price = symbolicPrice[tokenIn][tokenOut][block.timestamp];
            // No need for checked math as we are checking it manually beforehand
            // Always round up the expected min amount out. Limit amount is slippage.
            minAmountOut = symbolicMinAmount[price][amountIn];
        } else {
            revert('SWAP_INVALID_LIMIT_TYPE');
        }

        uint256 preBalanceIn = IERC20(tokenIn).balanceOf(address(this));
        uint256 preBalanceOut = IERC20(tokenOut).balanceOf(address(this));
        
        IERC20(tokenIn).transfer(dex, amountIn);
        IERC20(tokenOut).transferFrom(dex, address(this), symbolicAmounOut[random]);

        uint256 postBalanceIn = IERC20(tokenIn).balanceOf(address(this));
        require(postBalanceIn >= preBalanceIn - amountIn, 'SWAP_BAD_TOKEN_IN_BALANCE');

        uint256 amountOutBeforeFees = IERC20(tokenOut).balanceOf(address(this)) - preBalanceOut;
        require(amountOutBeforeFees >= minAmountOut, 'SWAP_MIN_AMOUNT');

        uint256 swapFeeAmount = symbolicFeeAmount[tokenIn][amountIn];
        amountOut = amountOutBeforeFees - swapFeeAmount;
        //prepare for other call
        random++; 
        
    }

    function withdraw(address token, uint256 amount, address recipient, bytes memory data)
        external override returns (uint256 withdrawn) {
             IERC20(token).transfer(recipient,amount);
             return amount;
    }


}
