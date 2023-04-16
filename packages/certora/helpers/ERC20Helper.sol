// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.0;

import {IERC20} from '@openzeppelin/contracts/token/ERC20/IERC20.sol';
contract ERC20Helper  {
    function getTokenBalanceOf(address t, address a) external view returns (uint256) {
        return IERC20(t).balanceOf(a);
    }
}