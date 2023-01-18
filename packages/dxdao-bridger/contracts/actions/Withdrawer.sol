// SPDX-License-Identifier: GPL-3.0-or-later
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

pragma solidity ^0.8.0;

import '@mimic-fi/v2-smart-vaults-base/contracts/actions/BaseAction.sol';
import '@mimic-fi/v2-smart-vaults-base/contracts/actions/RelayedAction.sol';
import '@mimic-fi/v2-smart-vaults-base/contracts/actions/TokenThresholdAction.sol';
import '@mimic-fi/v2-smart-vaults-base/contracts/actions/WithdrawalAction.sol';

contract Withdrawer is BaseAction, RelayedAction, TokenThresholdAction, WithdrawalAction {
    // Base gas amount charged to cover gas payment
    uint256 public constant override BASE_GAS = 110e3;

    constructor(address admin, address registry) BaseAction(admin, registry) {
        // solhint-disable-previous-line no-empty-blocks
    }

    function canExecute(address token) external view returns (bool) {
        return _passesThreshold(token, _balanceOf(token));
    }

    function call(address token) external auth nonReentrant {
        isRelayer[msg.sender] ? _relayedCall(token) : _call(token);
        _withdraw(Denominations.isNativeToken(token) ? smartVault.wrappedNativeToken() : token);
    }

    function _relayedCall(address token) internal redeemGas {
        _call(token);
    }

    function _call(address token) internal {
        uint256 balance = _balanceOf(token);
        _validateThreshold(token, balance);
        if (Denominations.isNativeToken(token)) smartVault.wrap(balance, new bytes(0));
        emit Executed();
    }
}