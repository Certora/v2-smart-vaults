/// @dev Spec file to include all basic methods of the project

using SmartVault as SV
/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods {
    /// erc20 spec
    /// @notice: dispatched methods do not require a contract prefix.
    balanceOf(address) returns (uint256) => DISPATCHER(true)
    allowance(address,address) returns (uint) => DISPATCHER(true)
    approve(address,uint256) returns (bool) => DISPATCHER(true)
    transfer(address,uint256) returns (bool) => DISPATCHER(true)
    transferFrom(address,address,uint256) returns (bool) => DISPATCHER(true)

    /// SmartVault Fees
    SV.withdrawFee() envfree;
    SV.performanceFee() envfree;
    SV.swapFee() envfree;
    SV.bridgeFee() envfree;

    /// Base action
    smartVault() returns (address) envfree;
}
