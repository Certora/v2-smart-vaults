certoraRun ./packages/balancer-fee-collector/contracts/actions/withdraw/Withdrawer.sol \
    ./packages/certora/helpers/SymbolicSmartVault.sol \
    ./packages/certora/helpers/ProtocolFeeWithdrawerMock.sol \
    ./node_modules/@mimic-fi/v2-price-oracle/contracts/oracle/PriceOracle.sol \
    ./packages/certora/helpers/ERC20_A.sol \
    ./packages/certora/helpers/ERC20_B.sol \
--verify Withdrawer:./packages/certora/specs/Withdrawer.spec \
--link \
    Withdrawer:smartVault=SymbolicSmartVault \
--packages @openzeppelin=node_modules/@openzeppelin @mimic-fi=node_modules/@mimic-fi @chainlink=node_modules/@chainlink \
--path . \
--send_only \
--cloud pre_cvl2 \
--loop_iter 3 \
--optimistic_loop \
--settings -optimisticUnboundedHashing=true,-copyLoopUnroll=8 \
--msg "Withdrawer sanity"


#sanity https://prover.certora.com/output/47234/32a33e9084d948b2bb8f036758cf1f20?anonymousKey=0360c117d26be751f909a61b72a298d2c7d9d70a
#sanity w SymbolicSmartVault  https://prover.certora.com/output/47234/33a956298ba242e0b395bd2814572248?anonymousKey=64ec9ddb437f818d4adc3440ae115b956b6af910