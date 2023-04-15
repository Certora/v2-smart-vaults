certoraRun ./packages/balancer-fee-collector/contracts/actions/claim/Claimer.sol \
    ./packages/certora/munged/SmartVault.sol \
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


#sanity with high TO https://prover.certora.com/output/47234/ba03f62e52f54d9d92d69754b66a685b?anonymousKey=4f38709d03a16d00fcb8fe1dee13dbd9f9972732