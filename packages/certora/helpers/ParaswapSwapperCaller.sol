// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.0;

import {ParaswapSwapper} from "../../balancer-fee-collector/contracts/actions/swap/ParaswapSwapper.sol";

contract ParaswapSwapperCaller {
    constructor(address _swapper) {
        swapper = ParaswapSwapper(_swapper);
    }

    ParaswapSwapper public immutable swapper;

    function callSwapper(
        address tokenIn,
        uint256 amountIn,
        uint256 minAmountOut,
        uint256 expectedAmountOut,
        uint256 deadline,
        bytes memory data,
        bytes memory sig
    ) public {
        swapper.call(
            tokenIn,
            amountIn,
            minAmountOut,
            expectedAmountOut,
            deadline,
            data,
            sig);
    }
}