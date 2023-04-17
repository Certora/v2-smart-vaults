// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.0;

import {IProtocolFeeWithdrawer} from '../../balancer-fee-collector/contracts/actions/claim/IProtocolFeeWithdrawer.sol';

contract ProtocolFeeWithdrawerMock is IProtocolFeeWithdrawer {

    function withdrawCollectedFees(address[] calldata tokens, uint256[] calldata amounts, address recipient) external override {
        //nop
    }

}