// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.0;

import {SmartVault} from '../munged/SmartVault.sol';
contract SmartVaultHarness is SmartVault {
    
    mapping (address => mapping(uint256 => uint256)) private _symbolicFeeAmount;
    
    /**
     * @dev Creates a new Smart Vault implementation with references that should be shared among all implementations
     * @param _wrappedNativeToken Address of the wrapped native token to be used
     * @param _registry Address of the Mimic Registry to be referenced
     */
    constructor(address _wrappedNativeToken, address _registry) SmartVault(_wrappedNativeToken,_registry) {}

    /**
     * @dev Internal function to pay the amount of fees to be charged based on a fee configuration to the fee collector
     * @notice Certora simplification : uses a symbolic (arbitrary) fee amount.
     * @param token Token being charged
     * @param amount Token amount to be taxed with fees
     * @param fee Fee configuration to be applied
     * @return paidAmount Amount of fees paid to the fee collector
     */
    function _payFee(address token, uint256 amount, Fee storage fee) internal override returns (uint256 paidAmount) {
        // If cap amount or cap period are not set, charge the entire amount
        if (fee.token == address(0) || fee.cap == 0 || fee.period == 0) {
            uint256 feeAmount = amount * fee.pct;
            _safeTransfer(token, feeCollector, feeAmount);
            return feeAmount;
        }
        paidAmount = _symbolicFeeAmount[token][amount];

        // Pay fee amount to the fee collector
        _safeTransfer(token, feeCollector, paidAmount);
    }

    function payFee(address token, uint256 amount) external returns (uint256) {
        return _payFee(token, amount, swapFee);
    }
}