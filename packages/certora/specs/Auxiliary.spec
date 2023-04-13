using SmartVault as SV

/**************************************************
 *                GHOSTS AND HOOKS                *
 **************************************************/
definition maxSig() returns bytes4 = 0xffffffff00000000000000000000000000000000000000000000000000000000;
definition maxAddress() returns address = 0xffffffffffffffffffffffffffffffffffffffff;
definition ANY_ADDRESS() returns address = 0xFFfFfFffFFfffFFfFFfFFFFFffFFFffffFfFFFfF;

definition setPriceFeed_sig() returns bytes4 = 0x67a1d5ab;

/// Authorized mirrored mapping (Paraswapper)
ghost mapping(address => mapping(bytes4 => bool)) ghostAuthorized_Swapper {
    init_state axiom forall address x. forall bytes4 y.
        ghostAuthorized_Swapper[x][y] == false;
}

hook Sstore authorized[KEY address who][KEY bytes4 what] bool value (bool old_value) STORAGE {
    bytes4 what_ = (what & maxSig()) >> 224;
    address who_ = who & maxAddress();
    ghostAuthorized_Swapper[who_][what_] = value; 
}

hook Sload bool value authorized[KEY address who][KEY bytes4 what] STORAGE {
    bytes4 what_ = (what & maxSig()) >> 224;
    address who_ = who & maxAddress();
    require ghostAuthorized_Swapper[who_][what_] == value; 
}

/// Authorized mirrored mapping (SmartVault)
ghost mapping(address => mapping(bytes4 => bool)) ghostAuthorized_Vault {
    init_state axiom forall address x. forall bytes4 y.
        ghostAuthorized_Vault[x][y] == false;
}

hook Sstore SV.authorized[KEY address who][KEY bytes4 what] bool value (bool old_value) STORAGE {
    bytes4 what_ = (what & maxSig()) >> 224;
    address who_ = who & maxAddress();
    ghostAuthorized_Vault[who_][what_] = value; 
}

hook Sload bool value SV.authorized[KEY address who][KEY bytes4 what] STORAGE {
    bytes4 what_ = (what & maxSig()) >> 224;
    address who_ = who & maxAddress();
    require ghostAuthorized_Vault[who_][what_] == value; 
}

/**************************************************
 *               CVL FUNCS                        *
 **************************************************/
/// A helper function to set a unique authorized address (who)
/// for some specific function signature (what).
function singleAddressAuthorization_vault(address who, bytes4 what) {
    require forall address user. (user != who=> !ghostAuthorized_Vault[user][what]);
    require !ghostAuthorized_Vault[ANY_ADDRESS()][what];
}

/// A helper function to set two unique authorized addresses (who1, who2)
/// for some specific function signature (what).
function doubleAddressAuthorization_vault(address who1, address who2, bytes4 what) {
    require forall address user. ( (user != who1 && user != who2) => !ghostAuthorized_Vault[user][what]);
    require !ghostAuthorized_Vault[ANY_ADDRESS()][what];
}

/// A helper function to set a unique authorized address (who)
/// for **any** function signature (what)
function singleAddressGetsTotalControl_vault(address who) {
    require forall address user.
                forall bytes4 func_sig. (user != who => !ghostAuthorized_Vault[user][func_sig]);
    require forall bytes4 func_sig. (!ghostAuthorized_Vault[ANY_ADDRESS()][func_sig]);
}
