
using ERC20Helper as helper;
using SymbolicSmartVault as symbolicVault;

methods {

    function _.balanceOf(address) external          => DISPATCHER(true);
    function _.allowance(address,address) external  => DISPATCHER(true);
    function _.approve(address,uint256) external    => DISPATCHER(true);
    function _.transfer(address,uint256) external   => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    function SymbolicSmartVault.dex() external returns (address)  envfree;
    function helper.getTokenBalanceOf(address, address) external returns (uint256) envfree;

    function smartVault() external returns (address) envfree;


    function tokenOut() external returns (address) envfree;
    function swapSigner() external returns (address) envfree;
    function defaultMaxSlippage() external returns (uint256) envfree;
    function tokenMaxSlippages(address) external returns (uint256) envfree;


}

/**************************************************
 *              DEFINITIONS                     *
 **************************************************/
definition MAX_FEE_PCT() returns uint256 = 1000000000000000000;

/**************************************************
 *              MISC RULES                     *
 **************************************************/


rule sanity(method f) {
    env e;
    calldataarg args;
    f(e, args);
    assert false;
}


/**************************************************
 *              SWAP INTEGRITY RULES              *
 **************************************************/
/// Correctness of balance updates in tokenIn by swap()
rule swapIntegrityTokenIn() {
    env e;
    /// swap (call) parameters
    address tokenIn ;
    uint256 amountIn;
    uint256 minAmountOut;
    uint256 expectedAmountOut;
    uint256 deadline;
    bytes data;
    bytes signature;

    require smartVault() == symbolicVault; 

    require symbolicVault.dex() != symbolicVault;
    uint256 balanceInSmartVaultBefore = helper.getTokenBalanceOf(tokenIn,symbolicVault);

    call(e, tokenIn, amountIn, minAmountOut,
            expectedAmountOut, deadline, data, signature);

    uint256 balanceInSmartVaultAfter = helper.getTokenBalanceOf(tokenIn,symbolicVault);

    assert balanceInSmartVaultBefore - balanceInSmartVaultAfter == to_mathint(amountIn), "SmartVault balance should be decreased by amountIn";
}