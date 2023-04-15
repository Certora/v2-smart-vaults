certoraRun ./packages/balancer-fee-collector/contracts/actions/withdraw/Withdrawer.sol \
    ./packages/certora/munged/SmartVault.sol \
    ./packages/certora/helpers/ProtocolFeeWithdrawerMock.sol \
    ./node_modules/@mimic-fi/v2-price-oracle/contracts/oracle/PriceOracle.sol \
    ./packages/certora/helpers/ERC20_A.sol \
    ./packages/certora/helpers/ERC20_B.sol \
--verify Withdrawer:./packages/certora/specs/Withdrawer.spec \
--link \
    Withdrawer:smartVault=SmartVault \
    SmartVault:priceOracle=PriceOracle \
--packages @openzeppelin=node_modules/@openzeppelin @mimic-fi=node_modules/@mimic-fi @chainlink=node_modules/@chainlink \
--path . \
--send_only \
--cloud pre_cvl2 \
--loop_iter 3 \
--optimistic_loop \
--settings -optimisticUnboundedHashing=true,-copyLoopUnroll=8 \
--msg "Withdrawer sanity"


#sanity https://prover.certora.com/output/47234/589c41b88b5b4c5da0959e521818103c?anonymousKey=5fc0415a9a93315cdb9e1a03eb00da24106e27bd