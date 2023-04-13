import "./Auxiliary.spec"
import "./BaseMethods.spec"

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