using ERC20Helper as helper;
using SymbolicSmartVault as symbolicVault;

methods {

    function _.balanceOf(address) external          => DISPATCHER(true);
    function _.allowance(address,address) external  => DISPATCHER(true);
    function _.approve(address,uint256) external    => DISPATCHER(true);
    function _.transfer(address,uint256) external   => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    function _.swap(uint8,address,address,uint256,uint8,uint256,bytes) external => DISPATCHER(true);
    function _.withdraw(address,uint256,address,bytes) external => DISPATCHER(true);

    function SymbolicSmartVault.dex() external returns (address)  envfree;
    function helper.getTokenBalanceOf(address, address) external returns (uint256) envfree;
    function helper.castUint32ToBytes4(uint32) external returns (bytes4) envfree;

    function smartVault() external returns (address) envfree;


    function tokenOut() external returns (address) envfree;
    function swapSigner() external returns (address) envfree;
    function defaultMaxSlippage() external returns (uint256) envfree;
    function tokenMaxSlippages(address) external returns (uint256) envfree;

    function isAuthorized(address,bytes4) external returns (bool) envfree;
    function getTokenSlippage(address) external returns (uint256) envfree;
    function isTokenDenied(address) external returns (bool) envfree;
}

/**************************************************
 *              DEFINITIONS                     *
 **************************************************/
definition MAX_FEE_PCT() returns uint256 = 1000000000000000000;

// GHOST COPIES
ghost mapping(uint256 => bytes32) ghostValues {
    init_state axiom forall uint256 x. ghostValues[x] == 0;
}
ghost mapping(bytes32 => uint256) ghostIndexes {
    init_state axiom forall bytes32 x. ghostIndexes[x] == 0;
}
ghost uint256 ghostLength {
    // assumption: it's infeasible to grow the list to these many elements.
    axiom ghostLength < 0xffffffffffffffffffffffffffffffff;
}

// HOOKS
hook Sstore currentContract.deniedTokens.(offset 0) uint256 newLength STORAGE {
    ghostLength = newLength;
}
hook Sstore currentContract.deniedTokens._inner._values[INDEX uint256 index] bytes32 newValue STORAGE {
    ghostValues[index] = newValue;
}
hook Sstore currentContract.deniedTokens._inner._indexes[KEY bytes32 value] uint256 newIndex STORAGE {
    ghostIndexes[value] = newIndex;
}
hook Sload uint256 length currentContract.deniedTokens.(offset 0) STORAGE {
    require ghostLength == length;
}
hook Sload bytes32 value currentContract.deniedTokens._inner._values[INDEX uint256 index] STORAGE {
    require ghostValues[index] == value;
}
hook Sload uint256 index currentContract.deniedTokens._inner._indexes[KEY bytes32 value] STORAGE {
    require ghostIndexes[value] == index;
}

// INVARIANTS

invariant setInvariant()
    (forall uint256 index. 0 <= index && index < ghostLength => to_mathint(ghostIndexes[ghostValues[index]]) == index + 1)
    && (forall bytes32 value. ghostIndexes[value] == 0 || 
         ((forall uint256 tmp. to_mathint(tmp) == (ghostIndexes[value] - 1) => ghostValues[tmp] == value)
          && ghostIndexes[value] >= 1 && ghostIndexes[value] <= ghostLength))


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

rule maxSlippageSetterAuth(address tokenIn) {
    env e;
    method f;

    uint256 maxSlippageBefore = getTokenSlippage(tokenIn);

    calldataarg args;
    f(e, args);

    uint256 maxSlippageAfter = getTokenSlippage(tokenIn);

    assert maxSlippageAfter != maxSlippageBefore => isAuthorized(e.msg.sender, helper.castUint32ToBytes4(f.selector));
}


rule doNotForgetAuthModifier(method f) filtered  {
    f -> !f.isView
} {
    env e;

    bool isAuthorizedBefore = isAuthorized(e.msg.sender, helper.castUint32ToBytes4(f.selector));

    calldataarg args;
    f(e, args);

    assert isAuthorizedBefore;
}

rule frontRunning(method f, method g)  filtered { f-> !f.isView, g -> !g.isView}
{
	env e1;
	calldataarg arg;

	storage initialStorage = lastStorage;
	f(e1, arg);

	env e2;
	calldataarg arg2;
	require e2.msg.sender != e1.msg.sender;
	g(e2, arg2) at initialStorage; 
	f@withrevert(e1, arg);
	bool succeeded = !lastReverted;

	assert succeeded, "${f.selector} can be not be called if ${g.selector} was called before";
}

rule deniedTokens(address tokenA, address tokenB, address tokenC) {
    env e1;
    bool deniedA;
    bool deniedB;

    requireInvariant setInvariant;
    require tokenA != tokenB;

    storage initialStorage = lastStorage;
    setDeniedTokens(e1, [tokenA, tokenB], [deniedA, deniedB]);

    bool deniedC1 = isTokenDenied(tokenC);

    env e2;
    setDeniedTokens(e2, [tokenB, tokenA], [deniedB, deniedA]) at initialStorage;
    
    bool deniedC2 = isTokenDenied(tokenC);
    assert deniedC1 == deniedC2;
}
