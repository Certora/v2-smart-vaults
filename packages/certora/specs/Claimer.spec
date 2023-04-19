// using SymbolicSmartVault as ssv;

methods {
    function _.balanceOf(address) external          => DISPATCHER(true);
    function _.allowance(address,address) external  => DISPATCHER(true);
    function _.approve(address,uint256) external    => DISPATCHER(true);
    function _.transfer(address,uint256) external   => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);
    
    // function SymbolicSmartVault.claimingToken() external returns (address) envfree;
    // function SymbolicSmartVault.claimingAmount() external returns (uint256) envfree;
    function _.call(address, bytes, uint256, bytes) external => NONDET;

    function getClaimableBalance(address) external returns (uint256) envfree;
    function _buildData(address token, uint256 amount) internal returns (bytes memory) => NONDET;

    function _.withdrawCollectedFees(address[], uint256[], address) external => NONDET;
}

rule sanity(method f) filtered { f -> f.selector != sig:call(address).selector } {
    env e;
    calldataarg args;
    f(e, args);
    assert(false);
}

rule sanityCall() {
    address token;
    // require(ssv.claimingToken() == token);
    // require(getClaimableBalance(token) == ssv.claimingAmount());

    env e;
    call(e, token);
    assert(false);
}