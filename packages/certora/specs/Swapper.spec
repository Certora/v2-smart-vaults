import "./Auxiliary.spec";

using ERC20_A as erc20A;
using ERC20_B as erc20B;

methods {
    // Paraswap Swapper
    /// @notice: External/public methods of the main contract do not require its name as a prefix.
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
rule testSingleAuthorization() {
    env e1; 
    env e2;
    calldataarg args1;
    calldataarg args2;
    bytes4 what = setPriceFeed_sig();
    //singleAddressAuthorization_vault(e1.msg.sender, what);
    require !ghostAuthorized_Vault[ANYADDRESS()][what];
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
    //doubleAddressAuthorization_vault(e1.msg.sender, almighty, what);
    require !ghostAuthorized_Vault[ANYADDRESS()][what];
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
    swapFee_token != 0

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
    bytes Sig;

    address vault = smartVault();

    uint256 balanceInSmartVaultBefore = helper.getTokenBalanceOf(tokenIn, vault);

    call(e, tokenIn, amountIn, minAmountOut,
            expectedAmountOut, deadline, data, Sig);

    uint256 balanceInSmartVaultAfter = helper.getTokenBalanceOf(tokenIn, vault);

    assert balanceInSmartVaultBefore - balanceInSmartVaultAfter == to_mathint(amountIn), "SmartVault balance should be decreased by amountIn";
}

rule swapperRevert() {
    env e;
    address tokenIn;
    address tokenOut = tokenOut();
    uint256 amountIn;
    uint256 minAmountOut;
    uint256 expectedAmountOut;
    uint256 deadline;
    bytes data;
    bytes Sig;

    call@withrevert(e, tokenIn, amountIn, minAmountOut,
            expectedAmountOut, deadline, data, Sig);

    bool swap_reverted = lastReverted;

    assert tokenIn == tokenOut => swap_reverted;
    assert tokenIn == 0 => swap_reverted;
    assert expectedAmountOut < minAmountOut => swap_reverted;
}