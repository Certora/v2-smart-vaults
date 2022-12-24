import { assertIndirectEvent, instanceAt } from '@mimic-fi/v2-helpers'
import { ARTIFACTS, deployment } from '@mimic-fi/v2-smart-vaults-base'

/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
/* eslint-disable no-unused-vars */

export default async (input: any, writeOutput: (key: string, value: string) => void): Promise<void> => {
  const { params, mimic } = input

  const create3Factory = await instanceAt(ARTIFACTS.CREATE3_FACTORY, mimic.Create3Factory)
  const deployer = await deployment.create3(input.namespace, 'v1', create3Factory, 'L1SmartVaultDeployer', [], null, {
    Deployer: mimic.Deployer,
  })
  writeOutput('L1Deployer', deployer.address)

  const bridger = await deployment.create3(input.namespace, 'v1', create3Factory, 'L1HopBridger', [
    deployer.address,
    mimic.Registry,
  ])
  writeOutput('L1HopBridger', bridger.address)
  params.l1HopBridgerActionParams.impl = bridger.address

  const tx = await deployer.deploy(params)
  const registry = await instanceAt('IRegistry', mimic.Registry)
  const event = await assertIndirectEvent(tx, registry.interface, 'Cloned', { implementation: mimic.SmartVault })
  writeOutput('SmartVault', event.args.instance)
}
