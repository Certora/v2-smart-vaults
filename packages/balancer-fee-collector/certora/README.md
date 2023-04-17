

# Verification of balancer-fee-collector/contracts/actions/swap/ParaswapSwapper.sol  
How to run:

certoraRun packages/certora/conf/paraSwapSwapper.conf

Uses a symbolicVault defined in packages/certora/helpers/SymbolicSmartVault.sol and proven with
certoraRun packages/certora/conf/symbolicSmartVaultCheck.conf
and according to verification of smartVault in https://github.com/Certora/v2-core/blob/certoraNew/certora/specs



using CVL2 see: 
https://docs.certora.com/en/cvl_rewrite-main/docs/cvl/cvl2/changes.html