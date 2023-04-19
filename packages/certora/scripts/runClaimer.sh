certoraRun packages/certora/conf/claimer.conf


#also wo calling the WithdrawerMock (905s) https://prover.certora.com/output/47234/444ae092a3164ad685370e904a2dcc02?anonymousKey=656a22c04cfd2ed7233f2e3569675214b23a5e05
#also wo the call to ssv.call (25s) https://prover.certora.com/output/47234/ddbeaf7fc67447ddb12bcf6337cb5d11?anonymousKey=e49029f0f7007bf7ba9b3a74426e82777d484c00
#w call to ssv.call w erc20 dispatchers (5744s) https://prover.certora.com/output/47234/cd71450beee140a284eb8994c83e70cc?anonymousKey=51abae92af8df0f1245129209a25e80a7bfaae8d
#same wo ERC20_B in the contracts list (1136s) https://prover.certora.com/output/47234/1830b985e39d41aea577f5323e525c44?anonymousKey=26bfa9aba0ee37047a2b13f94011dfd2dcb470d2
#no munging https://prover.certora.com/output/47234/e3e83ec8b3d3415aa3e179f4e6b1a787?anonymousKey=f3502451074533eae14afb75a985ca560601f130
#w linking claiming target https://prover.certora.com/output/47234/1b9f628495c143e5880fc5fdb07437b4?anonymousKey=fb9989a6a64ef86532003acc3650b701c2b7d9e4
# same wo calling _build https://prover.certora.com/output/47234/7c6f851e2e4848d69b4bcfcad5b85fbc?anonymousKey=7b519db3e98f8ad7c3e572ab467068c199e9a036
#same w summary for withdrawCollectedFees https://prover.certora.com/output/47234/e876e1f161a74174a8dfcacdc2fb4577?anonymousKey=157bcdf34089db95c064ab6fc10ecfdcc03973e9
#same w ssv::call commented out entirly (752s) https://prover.certora.com/output/47234/ae4d25bb40324368843845a5a158e932?anonymousKey=e40b141b9a4a2e17af124fa1557babb5d5817173
#wo ssv w summary for sv.call (203s) https://prover.certora.com/output/47234/f614614fc543465fb1ad05351787ea26?anonymousKey=a91e968575194dca750ecc6e3d2b294fd3916328