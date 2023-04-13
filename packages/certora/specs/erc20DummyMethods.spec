using ERC20_A as erc20A
using ERC20_B as erc20B
methods {
    erc20A.balanceOf(address) returns (uint256) envfree;
    erc20A.allowance(address,address) returns (uint256) envfree;
    erc20B.balanceOf(address) returns (uint256) envfree;
    erc20B.allowance(address,address) returns (uint256) envfree;
}
