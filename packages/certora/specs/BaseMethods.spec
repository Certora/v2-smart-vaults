/// @dev Spec file to include all basic methods of the project
using SmartVaultHarness as SV;
using ERC20Helper as helper;
using PriceOracle as oracle;
/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods {
    /// erc20 spec
    /// @notice: dispatched methods do not require a contract prefix.
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);
    function helper.getTokenBalanceOf(address, address) external returns(uint256) envfree;
    function oracle.uint32ToBytes4(uint32) external returns(bytes4) envfree;
    
    /// SmartVault Fees
    function SV.swapFee() external returns (uint256, uint256, address, uint256, uint256, uint256) envfree;
    function SV.withdrawFee() external returns (uint256, uint256, address, uint256, uint256, uint256) optional envfree;
    function SV.ANY_ADDRESS() external returns (address) envfree;
    function SV.setPriceFeed(address, address, address) external;

    /// Base action
    function smartVault() external returns (address) envfree;
}
