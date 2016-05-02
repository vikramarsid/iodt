import subprocess

from eth_contract.core import Contract

from config_map import ConfigMap
from web3_connect import web3

config = ConfigMap()


# ipc_path = expanduser("~") + "/iodt-node" + '/data/' + config.config_section_map("instance")['id'] + '/geth.ipc'
# web3 = Web3(IPCProvider(ipc_path, testnet=False))
# web3.config.defaultAccount = config.config_section_map("instance")["account"]
# web3.config.defaultBlock = "latest"


class PowerBartering:
    def __init__(self, mode):
        self.mode = mode

    def get_power_usage(self):
        command = "upower -i $(upower -e | grep BAT) | grep --color=never -E percentage|xargs|cut -d' ' -f2|sed s/%//"
        get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
        return get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")

    def limit_check(self):
        usage = int(self.get_power_usage())
        limit = int(config.config_section_map("userprofile")['powerlimit'])
        assert (usage == 0 & limit == 0), "***Usage and limit reported: 0 ***"
        if usage > limit:
            print "hi"
            Contract()

    def peer_usage(self):
        print "in peer usage"
        mid = config.config_section_map("instance")["shh_id"]
        if web3.shh.hasIdentity(mid):
            options = {"topics": ["0x696f64745f706f7765725f626172746572696e67"],
                       "payload": "0x73656e64506f7765725573616765"}
            web3.shh.post()


if __name__ == '__main__':
    pb = PowerBartering("active")
    print(pb.get_power_usage())
