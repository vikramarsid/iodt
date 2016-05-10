import sys

from config_map import ConfigMap
from web3 import Web3, RPCProvider

config = ConfigMap()
web3 = Web3(RPCProvider(host="127.0.0.1", port=config.config_section_map("device")["rpcport"]))
web3.config.defaultAccount = config.config_section_map("instance")["account"]
web3.config.defaultBlock = "latest"


class Web3Connect:
    def __init__(self):
        pass

    @staticmethod
    def set_identity():
        try:
            if config.config_section_map("instance")["shh_id"] == "":
                my_identity = web3.shh.newIdentity()
                config.write_config("instance", "shh_id", my_identity)
                return my_identity
            else:
                return config.config_section_map("instance")["shh_id"]
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise

    @staticmethod
    def connect_contract():
        # contracts
        abi = '[{"constant":false,"inputs":[{"name":"member","type":"address"}],"name":"removeMember","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"limit","type":"uint256"},{"name":"usage","type":"uint256"}],"name":"powerUsage","outputs":[{"name":"res","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"type":"function"},{"constant":true,"inputs":[],"name":"numTransactions","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"transactions","outputs":[{"name":"","type":"bytes"}],"type":"function"},{"constant":true,"inputs":[],"name":"getMembers","outputs":[{"name":"","type":"address[]"}],"type":"function"},{"constant":false,"inputs":[{"name":"recipient","type":"address"},{"name":"message","type":"bytes"}],"name":"send","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"member","type":"address"}],"name":"addMember","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"transaction","type":"bytes"}],"name":"addTransaction","outputs":[],"type":"function"},{"inputs":[],"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"id","type":"uint256"}],"name":"NewTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"recipient","type":"address"},{"indexed":false,"name":"message","type":"bytes"}],"name":"Message","type":"event"}]'
        contract_factory = web3.eth.contract(abi)
        contract = contract_factory.at("0xeb82930325966679877a23fbf098336366a207b0")
        return contract

    @staticmethod
    def connect():
        return web3
