import requests
import subprocess
import time

from flask import json

import web3_connect
from config_map import ConfigMap

config = ConfigMap()
set_web3 = web3_connect.Web3Connect()
web3 = set_web3.connect()
cc = set_web3.connect_contract()

# topics
iodt_power_bartering_topic = "0x696f64745f706f7765725f626172746572696e67"
power_usage_topic = "0x73656e64506f7765725573616765"


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
        if usage > limit:
            print("hi")
            # e = self.call_contract()
            e = self.peer_usage()
            return e

    def peer_usage(self):
        print("in peer usage")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = {"topics": [iodt_power_bartering_topic],
                       "payload": power_usage_topic,
                       "ttl": 100,
                       "to": "0x04a84f0bf6dac52d11a650a8e92ad3e01c78d39c605a23af11989edb32442af84953fb6b1f27c7b2c71119a49888ab20bdfc1e74bdf2c22deab22cfbff67ad3139",
                       "from": "0x0488599ffad025a7dafce51be0b1fcf7ef7994873b465e5696d5ba1d061821ea8ac7074b6682d6ea16f9445f74e12f42af1d29e8a3f558b56ceec3832c7610b814",
                       "priority": 1
                       }
            broadcast = web3.shh.post(options)
            return broadcast

    def set_filter(self):
        print("in set filter")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = {"topics": ['0x696f64745f706f7765725f626172746572696e67']}
            setf = web3.shh.newFilter(options)
            return setf

    def get_filter_changes(self):
        print("in get filter changes")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = "0x2"
            getf = web3.shh.getFilterChanges(options)
            return getf

    def call_contract(self):
        print("In contract call")
        try:
            d = cc.send('0xa6cf418b64c0c81bc70fde7e5445f513b1b4d890', '777')
            return d
        except IndexError as err:
            print(err)
            return []

    def get_peer_details(self):
        print("Getting Peer details - " + str(time.time()))
        url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        payload = {'device_id': config.config_section_map("device")['id']}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            print("Peer details: " + r.text)
            rest = json.loads(r.text)
            print ("###################" + rest["Devices"][0]["shh_id"])
        return rest


if __name__ == '__main__':
    pb = PowerBartering("active")
    print(pb.get_power_usage())
    print(pb.limit_check())
    print(pb.set_filter())
    print(pb.get_filter_changes())
    #print (pb.get_peer_details())
