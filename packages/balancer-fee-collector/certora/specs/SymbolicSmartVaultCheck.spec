/*
    This is a specification file for smart contract
    verification with the Certora prover.

    For more information,
    visit: https://www.certora.com/

    This file is run with command:
    
      certoraRun packages/certora/conf/symbolicSmartVaultCheck.conf 
    
    from the root of v2-smart-vaults 
*/


using ERC20Helper as helper;

/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods {

    ////////////////////////////////////////
	// ERC20 methods
    function _.balanceOf(address) external          => DISPATCHER(true);
    function _.allowance(address,address) external  => DISPATCHER(true);
    function _.approve(address,uint256) external    => DISPATCHER(true);
    function _.transfer(address,uint256) external   => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    function dex() external returns (address)  envfree;
    function helper.getTokenBalanceOf(address, address) external returns (uint256) envfree;
}

/**************************************************
 *                 SPECIFICATION                  *
 **************************************************/

 
// STATUS - verified
// Correctness of balance updates in tokenIn by swap()
rule swapIntergrityTokenIn(env e, env e2, method f) {
    // swap parameters
    uint8 source;
    address tokenIn;
    address tokenOut;
    uint256 amountIn;
    SymbolicSmartVault.SwapLimit limitType;
    uint256 limitAmount;
    bytes data;

    require dex() != currentContract; // safe assumption

    uint256 balanceInDexBefore = helper.getTokenBalanceOf(tokenIn, dex());
    uint256 balanceInSmartVaultBefore = helper.getTokenBalanceOf(tokenIn, currentContract);

    uint256 amountOut = swap(e2, source, tokenIn, tokenOut, amountIn, limitType, limitAmount, data);

    uint256 balanceInDexAfter = helper.getTokenBalanceOf(tokenIn, dex());
    uint256 balanceInSmartVaultAfter = helper.getTokenBalanceOf(tokenIn, currentContract);

    assert balanceInDexAfter - balanceInDexBefore == to_mathint(amountIn), "Dex balance should be increased by amountIn";
    assert balanceInSmartVaultBefore - balanceInSmartVaultAfter == to_mathint(amountIn), "SmartVault balance should be decreased by amountIn";
}
