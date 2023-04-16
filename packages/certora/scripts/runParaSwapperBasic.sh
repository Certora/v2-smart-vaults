certoraRun ./packages/certora/conf/paraSwapSwapper.conf

# certoraRun ./packages/balancer-fee-collector/contracts/actions/swap/ParaswapSwapper.sol \
#             ./packages/certora/helpers/ERC20_A.sol \
#             ./packages/certora/helpers/ERC20_B.sol \
#             ./packages/certora/helpers/SymbolicSmartVault.sol \
# --verify ParaswapSwapper:./packages/certora/specs/sanity.spec \
# --solc solc8.2 \
# --packages @openzeppelin=node_modules/@openzeppelin @mimic-fi=node_modules/@mimic-fi @chainlink=node_modules/@chainlink \
# --path . \
# --link \
#     ParaswapSwapper:smartVault=SymbolicSmartVault \
# \
# --send_only \
# --cloud pre_cvl2 \
# --loop_iter 3 \
# --optimistic_loop \
# --rule_sanity \
# --settings -optimisticUnboundedHashing=true,-copyLoopUnroll=8 \
# --msg "Mimic ParaswapSwapper"