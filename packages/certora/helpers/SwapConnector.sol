// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity >=0.8.0;

import '@openzeppelin/contracts/token/ERC20/IERC20.sol';
interface ISwapConnector {
    /**
     * @dev Swaps two tokens
     * @param source Source to execute the requested swap
     * @param tokenIn Token being sent
     * @param tokenOut Token being received
     * @param amountIn Amount of tokenIn being swapped
     * @param minAmountOut Minimum amount of tokenOut willing to receive
     * @param data Encoded data to specify different swap parameters depending on the source picked
     */
    function swap(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut,
        bytes memory data
    ) external returns (uint256 amountOut);
}

interface IMultiDex {
    /**
     * @dev Gets a general amount out from a dex pool
     * @param source Source to execute the requested swap
     * @param tokenIn Token being sent
     * @param tokenOut Token being received
     * @param amountIn Amount of tokenIn being swapped
     */
    function getDexAmountOut(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn) 
        external view returns (uint256 amountOut);

    function sourceDex(uint8 source) external view returns(address);
}

contract SwapConnector is ISwapConnector {
    
    address public immutable multiDex;

    constructor(address _multiDex) {
        multiDex = _multiDex;
    }

    function swap(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut,
        bytes memory
    ) external override returns (uint256 amountOut) {
        address _dex = getSourceDex(source);
        amountOut = IMultiDex(multiDex).getDexAmountOut(source, tokenIn, tokenOut, amountIn);
        IERC20(tokenIn).transfer(_dex, amountIn);
        IERC20(tokenOut).transferFrom(_dex, address(this), amountOut);
    }

    function getSourceDex(uint8 source) public view returns(address) {
        return IMultiDex(multiDex).sourceDex(source);
    }
}

contract MultiDex is IMultiDex {
    // Source => Dex address
    mapping(uint8 => address) public override sourceDex;
    // Dex => tokenIn => tokenOut => pool address
    mapping(address => mapping(address => mapping(address => address))) private pool;
    // Pool address => amountIn => timestamp => amountOut;
    mapping(address => mapping(uint256 => mapping(uint256 => uint32))) private poolSwap;

    function getDexAmountOut(
        uint8 source,
        address tokenIn,
        address tokenOut,
        uint256 amountIn) 
        external override view returns (uint256 amountOut) {
        address _dex = sourceDex[source];
        address _pool = pool[_dex][tokenIn][tokenOut];
        require(_pool != address(0) && _dex != address(0) ,"Invalid dex and pool addresses");
        amountOut = poolSwap[_pool][amountIn][uint32(block.timestamp)];
    }
}