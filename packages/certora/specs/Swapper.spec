import "./Auxiliary.spec"
import "./erc20DummyMethods.spec"

using ParaswapSwapperCaller as caller

methods {
    // Paraswap Swapper
    /// @notice: External/public methods of the main contract do not require its name as a prefix.
    tokenOut() returns (address) envfree;
    swapSigner() returns (address) envfree;
    defaultMaxSlippage() returns (uint256) envfree;
    tokenMaxSlippages(address) returns (uint256) envfree;
}

/**************************************************
 *              DEFINITIONS                     *
 **************************************************/
definition MAX_FEE_PCT() returns uint256 = 1000000000000000000;

/**************************************************
 *              MISC RULES                     *
 **************************************************/
rule testSingleAuthorization() {
    env e1; 
    env e2;
    calldataarg args1;
    calldataarg args2;
    bytes4 what = setPriceFeed_sig();
    singleAddressAuthorization_vault(e1.msg.sender, what);
    SV.setPriceFeed(e1, args1);
    SV.setPriceFeed(e2, args2);
    assert e1.msg.sender == e2.msg.sender;
}

rule testDoubleAuthorization() {
    env e1; 
    env e2;
    calldataarg args1;
    calldataarg args2;
    address almighty;
    bytes4 what = setPriceFeed_sig();
    doubleAddressAuthorization_vault(e1.msg.sender, almighty, what);
    SV.setPriceFeed(e1, args1);
    SV.setPriceFeed(e2, args2);
    assert e1.msg.sender == e2.msg.sender || e2.msg.sender == almighty;
}

rule sanity(method f) {
    env e;
    calldataarg args;
    f(e, args);
    assert false;
}

/**************************************************
 *              FEE RULES                        *
 **************************************************/
invariant SwapFeeLE100PCT()
   SwapFeeParameter(pct()) <= MAX_FEE_PCT()

invariant FeeTokenIsNonZero()
    swapFee_token != 0 && withdrawFee_token != 0

/**************************************************
 *              SWAP INTEGRITY RULES              *
 **************************************************/
/// Correctness of balance updates in tokenIn by swap()
rule swapIntergrityTokenIn() {
    env e;
    /// swap (call) parameters
    address tokenIn = erc20A;
    uint256 amountIn;
    uint256 minAmountOut;
    uint256 expectedAmountOut;
    uint256 deadline;
    bytes data;
    bytes sig;

    address vault = smartVault();

    uint256 balanceInSmartVaultBefore = erc20A.balanceOf(vault);

    caller.callSwapper(e, tokenIn, amountIn, minAmountOut,
            expectedAmountOut, deadline, data, sig);

    uint256 balanceInSmartVaultAfter = erc20A.balanceOf(vault);

    assert balanceInSmartVaultBefore - balanceInSmartVaultAfter == amountIn, "SmartVault balance should be decreased by amountIn";
}