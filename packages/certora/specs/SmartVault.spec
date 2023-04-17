
////////////////////////////////////////
// ERC20 methods
import "./erc20.spec";
/**************************************************
 *                LINKED CONTRACTS                *
 **************************************************/
// Declaration of contracts used in the spec

 using PriceOracle as oracle;
 using ERC20Helper as helper;
 using SymbolicSmartVault as SV;
 using ERC20_A as erc20A;
 using ERC20_B as erc20B;

/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods {
    ////////////////////////////////////////
    function SV.withdraw(address,uint256,address,bytes) external returns(uint256);
    function SV.swap(uint8,address,address,uint256,SymbolicSmartVault.SwapLimit,uint256,bytes) external returns (uint256);
    function SV.feeCollector() external returns (address) envfree;
    function SV.dex() external returns (address) envfree;
    function SV.getPrice(address, address) external returns (uint256);
    function SV.wrappedNativeToken() external returns (address) envfree;
    function isAuthorized(address, bytes4) external returns (bool) envfree;

    // Price oracle & helpers
    function oracle.pow10(uint256) external returns (uint256) envfree;
    function helper.getTokenBalanceOf(address, address) external returns(uint256) envfree;
    function oracle.uint32ToBytes4(uint32) external returns (bytes4) envfree;
    function helper.getERC20Allowance(address, address, address) external returns (uint256) envfree;
    function oracle.mulDownFP(uint256, uint256) external returns (uint256) envfree;

    //Native token helper
    function oracle.getNativeBalanceOf(address) external returns (uint256) envfree;
    function ANY_ADDRESS() external returns (address) envfree;
}

/**************************************************
 *                  DEFINITIONS                   *
 **************************************************/
definition select_setPriceFeed() returns uint32 = 0x67a1d5ab;
definition select_collect() returns uint32 = 0x5af547e6;
definition select_setStrategy() returns uint32 = 0xbaa82a34;
definition select_setPriceOracle() returns uint32 = 0x530e784f;
definition select_withdraw() returns uint32 = 0x9003afee;
definition select_wrap() returns uint32 = 0x109b3c83;
definition select_unwrap() returns uint32 = 0xb413148e;
definition select_setPriceFeeds() returns uint32 = 0x4ed31090;
// also we can use the following writing:
//definition select_setPriceFeeds() returns uint32 = sig:setPriceFeeds(address[],address[],address[]).selector;

/*
definition delegateCalls(method f) returns bool = 
    (f.selector == sig:join(address,address[],uint256[],uint256,bytes).selector ||
    f.selector == sig:claim(address,bytes).selector ||
    f.selector == sig:exit(address,address[],uint256[],uint256,bytes).selector ||
    f.selector == sig:swap(uint8,address,address,uint256,SymbolicSmartVault.SwapLimit,uint256,bytes).selector);
*/
definition FixedPoint_ONE() returns uint256 = 1000000000000000000;

/**************************************************
 *                GHOSTS AND HOOKS                *
 **************************************************/

ghost mapping(address => mapping(bytes4 => bool)) ghostAuthorized {
    init_state axiom forall address x. forall bytes4 y.
        ghostAuthorized[x][y] == false;
}

hook Sstore authorized[KEY address who][KEY bytes4 what] bool value (bool old_value) STORAGE {
    ghostAuthorized[who][what] = value; 
}

hook Sload bool value authorized[KEY address who][KEY bytes4 what] STORAGE {
    require ghostAuthorized[who][what] == value; 
} 

/**************************************************
 *               CVL FUNCS                        *
 **************************************************/

// A helper function to set a unique authorized address (who)
// for some specific function signature (what).
function singleAddressAuthorization(address who, bytes4 what) {
    require forall address user. (user != who => !ghostAuthorized[user][what]);
    require !ghostAuthorized[ANY_ADDRESS()][what];
}

// A helper function to set two unique authorized addresses (who1, who2)
// for some specific function signature (what).
function doubleAddressAuthorization(address who1, address who2, bytes4 what) {
    require forall address user. ( (user != who1 && user != who2) => !ghostAuthorized[user][what]);
    require !ghostAuthorized[ANY_ADDRESS()][what];
}

// A helper function to set a unique authorized address (who)
// for **any** function signature (what)
function singleAddressGetsTotalControl(address who) {
    require forall address user.
                forall bytes4 func_sig. (user != who => !ghostAuthorized[user][func_sig]);
    require forall bytes4 func_sig. (!ghostAuthorized[ANY_ADDRESS()][func_sig]);
}

/*
// Realistic value for the decimals (4<=dec<=27)
function requireValidDecimals(address token) {
    uint256 decimals = oracle.getERC20Decimals(token);
    require decimals >= 4 && decimals <= 27;
}

// Consistency of the decimals between the ERC20 definition for the quote,
// and the decimals from the chainlink oracle feed.
function matchDecimals(address base, address quote) {
    require oracle.getFeedDecimals(getPriceFeed(base, quote)) == 
        oracle.getERC20Decimals(quote);
}

function getFeedPrice(address base, address quote) returns uint256 {
    uint256 price;
    uint256 decimal;
    price, decimal = oracle._getFeedData(getPriceFeed(base, quote));
    return price;
}

// Condition to match mutual prices from chainlink price oracle
function matchMutualPrices(address base, address quote) returns bool {
    address feed1 = getPriceFeed(base, quote);
    address feed2 = getPriceFeed(quote, base);
    uint256 price1; uint256 dec1;
    uint256 price2; uint256 dec2;
    price1, dec1 = oracle._getFeedData(feed1);
    price2, dec2 = oracle._getFeedData(feed2);
    return (to_mathint(price1 * price2) == to_mathint(oracle.pow10(require_uint256(dec1 + dec2))));
}

// Forces the price feed provider to go through the pivot feed for
// a pair of tokens base, quote
function usePivotForPair(address base, address quote) {
    address pivot = oracle.pivot();
    require pivot != base && pivot != quote &&
    getPriceFeed(base, quote) == 0 && getPriceFeed(quote, base) == 0 &&
    getPriceFeed(base, pivot) != 0 && getPriceFeed(quote, pivot) != 0;
}
*/
/**************************************************
 *                 VALID STATES                   *
 **************************************************/
// Describe expressions over the system's variables
// that should always hold.
// Usually implemented via invariants 


/**************************************************
 *               STATE TRANSITIONS                *
 **************************************************/
// Describe validity of state changes by taking into
// account when something can change or who may change



/**************************************************
 *                METHOD INTEGRITY                *
 **************************************************/

rule withdrawTransferIntegrity(address token, address to, uint256 amount) {
    env e;
    bytes data;
    address anyToken;
    address anyUser;
    require anyToken != token;
    require anyUser != SV && anyUser != to;
    require token != 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE; // not a native token

    uint256 toBalance1 = helper.getTokenBalanceOf(token, to);
    uint256 vaultBalance1 = helper.getTokenBalanceOf(token, SV);
    uint256 toBalanceAny1 = helper.getTokenBalanceOf(anyToken, to);
    uint256 vaultBalanceAny1 = helper.getTokenBalanceOf(anyToken, SV);
    uint256 anyUserBalance1 = helper.getTokenBalanceOf(token, anyUser);

      uint256 withdrawn = SV.withdraw(e, token, amount, to, data);

    uint256 toBalance2 = helper.getTokenBalanceOf(token, to);
    uint256 vaultBalance2 = helper.getTokenBalanceOf(token, SV);
    uint256 toBalanceAny2 = helper.getTokenBalanceOf(anyToken, to);
    uint256 vaultBalanceAny2 = helper.getTokenBalanceOf(anyToken, SV);
    uint256 anyUserBalance2 = helper.getTokenBalanceOf(token, anyUser);

    if(to == SV) {
        assert toBalance2 == toBalance1;
    }
    else {
        assert toBalance2 == require_uint256(toBalance1 + amount);
        assert vaultBalance2 == require_uint256(vaultBalance1 - amount);
    }
    
    assert toBalanceAny1 == toBalanceAny2;
    assert vaultBalanceAny1 == vaultBalanceAny2;
    assert anyUserBalance1 == anyUserBalance2;
}

rule withdrawTransferIntegrityOfNativeToken(address nativeToken, address to, uint256 amount) {
    env e;
    bytes data;
    address anyToken;
    address anyUser;
    address WRToken = SV.wrappedNativeToken();
    require anyToken != nativeToken;
    require anyUser != SV && anyUser != to;
    require nativeToken == 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE; // explicitly a native token

    uint256 toBalance1 = oracle.getNativeBalanceOf(to);
    uint256 vaultBalance1 = oracle.getNativeBalanceOf(SV);
    uint256 toBalanceAny1 = helper.getTokenBalanceOf(anyToken, to);
    uint256 vaultBalanceAny1 = helper.getTokenBalanceOf(anyToken, SV);
    uint256 anyUserBalance1 = oracle.getNativeBalanceOf(anyUser);

        uint256 withdrawn = SV.withdraw(e, nativeToken, amount, to, data);

    uint256 toBalance2 = oracle.getNativeBalanceOf(to);
    uint256 vaultBalance2 = oracle.getNativeBalanceOf(SV);
    uint256 toBalanceAny2 = helper.getTokenBalanceOf(anyToken, to);
    uint256 vaultBalanceAny2 = helper.getTokenBalanceOf(anyToken, SV);
    uint256 anyUserBalance2 = oracle.getNativeBalanceOf(anyUser);

    if(to == SV) {
        assert toBalance2 == toBalance1;
    }
    else {
        assert toBalance2 == require_uint256(toBalance1 + amount);
        assert vaultBalance2 == require_uint256(vaultBalance1 - amount);
    }
    
    if(anyToken == WRToken && to == WRToken) {
        assert require_uint256(vaultBalanceAny2 - vaultBalanceAny1) == amount;
    }
    else {
        assert vaultBalanceAny1 == vaultBalanceAny2;
    }

    assert toBalanceAny1 == toBalanceAny2;
    assert anyUserBalance1 == anyUserBalance2;
}

/**************************************************
 *                      MISC                      *
 **************************************************/

// STATUS - verified
// During swap(), no additional tokens should be gain regarding tokenOut
rule swapConsistencyTokenOut(env e) {
    uint8 source;
    address tokenIn;
    address tokenOut;
    uint256 amountIn;
    SymbolicSmartVault.SwapLimit limitType;
    uint256 limitAmount;
    bytes data;
    address Dex = SV.dex();
    address feeCol = SV.feeCollector();

    require tokenIn == erc20A;
    require tokenOut == erc20B;
    require feeCol != Dex && feeCol != SV;

    uint256 balanceInDexBefore = helper.getTokenBalanceOf(erc20A,Dex);
    uint256 balanceInSmartWaltBefore = helper.getTokenBalanceOf(erc20B,SV);
    uint256 balanceFCBefore = helper.getTokenBalanceOf(erc20B,feeCol);

    uint256 amountOut = SV.swap(e, source, tokenIn, tokenOut, amountIn, limitType, limitAmount, data);
    
    uint256 balanceInDexAfter = helper.getTokenBalanceOf(erc20B, Dex);
    uint256 balanceInSmartWaltAfter = helper.getTokenBalanceOf(erc20B, SV);
    uint256 balanceFCAfter = helper.getTokenBalanceOf(erc20B,feeCol);

    assert balanceInDexBefore + balanceInSmartWaltBefore + balanceFCBefore == balanceInDexAfter + balanceInSmartWaltAfter + balanceFCAfter;
}
