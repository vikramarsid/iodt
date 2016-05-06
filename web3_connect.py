from web3 import Web3, RPCProvider

from config_map import ConfigMap

config = ConfigMap()
web3 = Web3(RPCProvider(host="127.0.0.1", port=config.config_section_map("device")["rpcport"]))
web3.config.defaultAccount = config.config_section_map("instance")["account"]
web3.config.defaultBlock = "latest"


class Web3Connect:
    def set_identity(self):
        myIdentity = web3.shh.newIdentity()
        config.write_config("instance", "shh_id", myIdentity)
        return myIdentity

    def connect(self):
        return web3
