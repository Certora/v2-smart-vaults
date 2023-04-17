methods {
    function add(bytes32) external returns (bool) envfree;
    function remove(bytes32) external returns (bool) envfree;
    function contains(bytes32) external returns (bool) envfree;
    function length() external returns (uint256) envfree;
    function elemAt(uint256) external returns (bytes32) envfree;
}

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

hook Sstore currentContract.set.(offset 0) uint256 newLength STORAGE {
    ghostLength = newLength;
}
hook Sstore currentContract.set._inner._values[INDEX uint256 index] bytes32 newValue STORAGE {
    ghostValues[index] = newValue;
}
hook Sstore currentContract.set._inner._indexes[KEY bytes32 value] uint256 newIndex STORAGE {
    ghostIndexes[value] = newIndex;
}

hook Sload uint256 length currentContract.set.(offset 0) STORAGE {
    require ghostLength == length;
}
hook Sload bytes32 value currentContract.set._inner._values[INDEX uint256 index] STORAGE {
    require ghostValues[index] == value;
}
hook Sload uint256 index currentContract.set._inner._indexes[KEY bytes32 value] STORAGE {
    require ghostIndexes[value] == index;
}

// INVARIANTS

invariant setInvariant()
    (forall uint256 index. 0 <= index && index < ghostLength => to_mathint(ghostIndexes[ghostValues[index]]) == index + 1)
    && (forall bytes32 value. ghostIndexes[value] == 0 || 
         (ghostValues[require_uint256(ghostIndexes[value] - 1)] == value
          && ghostIndexes[value] >= 1 && ghostIndexes[value] <= ghostLength))
