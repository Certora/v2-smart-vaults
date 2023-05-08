// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.7.0) (token/ERC20/ERC20.sol)

pragma solidity ^0.8.0;
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20_B is ERC20 {
    constructor(string memory name_, string memory symbol_) ERC20(name_,symbol_) {}
}