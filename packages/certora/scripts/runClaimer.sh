certoraRun ./packages/balancer-fee-collector/contracts/actions/claim/Claimer.sol \
    ./node_modules/@mimic-fi/v2-smart-vault/contracts/SmartVault.sol \
    ./packages/certora/helpers/ProtocolFeeWithdrawerMock.sol \
    ./node_modules/@mimic-fi/v2-price-oracle/contracts/oracle/PriceOracle.sol \
    ./packages/certora/helpers/ERC20_A.sol \
    ./packages/certora/helpers/ERC20_B.sol \
--verify Claimer:./packages/certora/specs/Claimer.spec \
--link \
    Claimer:smartVault=SmartVault \
    Claimer:protocolFeeWithdrawer=ProtocolFeeWithdrawerMock \
    SmartVault:priceOracle=PriceOracle \
--packages @openzeppelin=node_modules/@openzeppelin @mimic-fi=node_modules/@mimic-fi @chainlink=node_modules/@chainlink \
--path . \
--send_only \
--cloud pre_cvl2 \
--loop_iter 3 \
--optimistic_loop \
--settings -optimisticUnboundedHashing=true,-copyLoopUnroll=8,-t=800,-mediumTimeout=20,-depth=20 \
--msg "Claimer sanity"


#sanity with high TO https://prover.certora.com/output/47234/8a17586683054dd79a0221ad91e9420a?anonymousKey=2c9aa2c313eba6c7d5c941808214880df79a3dd5