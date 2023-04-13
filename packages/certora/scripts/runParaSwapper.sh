certoraRun ./packages/balancer-fee-collector/contracts/actions/swap/ParaswapSwapper.sol \
            ./packages/certora/munged/SmartVault.sol \
--verify ParaswapSwapper:./packages/certora/specs/Swapper.spec \
--link ParaswapSwapper:smartVault=SmartVault \
--solc solc8.2 \
--send_only \
--cloud pre_cvl2 \
--loop_iter 3 \
--optimistic_loop \
--rule_sanity \
--settings -copyLoopUnroll=8 \
--msg "Mimic ParaswapSwapper"