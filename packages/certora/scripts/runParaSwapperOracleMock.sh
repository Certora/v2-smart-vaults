

certoraRun ./packages/balancer-fee-collector/contracts/actions/swap/ParaswapSwapper.sol \
            ./packages/certora/munged/SmartVault.sol \
            ./packages/certora/helpers/ERC20_A.sol \
            ./packages/certora/helpers/ERC20_B.sol \
            ./packages/certora/helpers/PriceOracle.sol \
--verify ParaswapSwapper:./packages/certora/specs/Swapper.spec \
--link \
    ParaswapSwapper:smartVault=SmartVault \
    SmartVault:priceOracle=PriceOracle \
\
--solc solc8.2 \
--packages @openzeppelin=node_modules/@openzeppelin @mimic-fi=node_modules/@mimic-fi @chainlink=node_modules/@chainlink \
--path . \
\
--send_only \
--cloud pre_cvl2 \
--loop_iter 3 \
--optimistic_loop \
--rule_sanity \
--rule sanity \
--settings -optimisticUnboundedHashing=true,-copyLoopUnroll=8 \
--msg "Mimic ParaswapSwapper"