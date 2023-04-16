
import "./Auxiliary.spec"
import "./erc20DummyMethods.spec"



rule sanity() {
    env e;
    calldataarg args;
    method f;
    f(e, args);
    assert(false);
} 