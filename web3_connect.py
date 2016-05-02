from os.path import expanduser

from web3 import Web3, IPCProvider

from config_map import ConfigMap

config = ConfigMap()
ipc_path = expanduser("~") + "/iodt-node" + '/data/' + config.config_section_map("instance")['id'] + '/geth.ipc'
web3 = Web3(IPCProvider(ipc_path, testnet=False))
web3.config.defaultAccount = config.config_section_map("instance")["account"]
web3.config.defaultBlock = "latest"


class Web3Connect:
    def set_identity(self):
        myIdentity = web3.shh.newIdentity()
        config.write_config("instance", "shh_id", myIdentity)
        return myIdentity

    def connect(self):
        return web3
