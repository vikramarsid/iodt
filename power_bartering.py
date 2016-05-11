# POWER BARTERING FACILITY
# 0. Initialize shh by setting the filters for topics {iodt_req_topic} {iodt_res_topic}
# 1. Start Listening for messages having {iodt_res_topic} as topic.
# 2. Start Power Bartering (Should be enabled based on the mode)
# 3. Check Usage limit
# 4. If usage is more than limit
# 5. Send broadcast message to peers, querying their usage
# 6. Start polling for changes
# 7. After receiving messages from all peers, flush the queue by shh_getMessage

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
iodt_req_topic = "0x696f64745f706f7765725f626172746572696e67"
iodt_res_topic = "0x5265706c792d506f7765725573616765496e666f"
power_usage_payload = "0x73656e64506f7765725573616765"
peer_shh_ids = []
peer_contract_ids = []
dict_req = {}
dict_res = {}
dict_post = {}

class PowerBartering:
    def __init__(self, mode):
        self.mode = mode

    @staticmethod
    def get_power_usage():
        command = "upower -i $(upower -e | grep BAT) | grep --color=never -E percentage|xargs|cut -d' ' -f2|sed s/%//"
        get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
        return get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")

    def limit_check(self):
        usage = int(self.get_power_usage())
        limit = int(config.config_section_map("userprofile")['powerlimit'])
        if usage > limit:
            e = self.get_peer_usage("shh")
            return "Completed Power Sync Job" + str(e)
        return "Usage under limit - Power Sync not needed"

    def get_peer_usage(self, stype):
        print("Getting Peer details - " + str(time.time()))
        # url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        url = "http://www.mocky.io/v2/5730e1fd100000ad0717f882"
        payload = {'device_id': config.config_section_map("device")['id']}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            rest = json.loads(r.text)
            if stype == "shh":
                for device in rest["Devices"]:
                    peer_shh_ids.append(device["shh_id"])
                if peer_shh_ids.__len__() > 0:
                    print ("Broadcasting Power Requirements\n")
                    self.broadcast_message()

            if stype == "contract":
                for device in rest["Devices"]:
                    peer_contract_ids.append(device["contract_addr"])
                print ("Peer Contract Addresses\n" + str(peer_contract_ids))
            return rest

    def broadcast_message(self):
        print("in broadcast message")
        success = 0
        fail = 0
        peers = peer_shh_ids.__len__()
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        if peers > 0:
            for ids in peer_shh_ids:
                status = self.post_message(iodt_req_topic, power_usage_payload, ids, mid)
                if status:
                    success += 1
                else:
                    fail += 1
        print ("\nTotal messages sent to peers: " + str(peers) + "\nTotal successful delivery : " + str(
            success) + "\nTotal un-successful delivery: " + str(fail))
        if success > 1:
            return "True"
        else:
            return "False"

    @staticmethod
    def post_message(topics, payload, tos, froms):
        try:
            print("in post message")
            mid = config.config_section_map("instance")["shh_id"]
            if mid == '':
                mid = set_web3.set_identity()
            if web3.shh.hasIdentity(mid):
                options = {"topics": [topics],
                           "payload": payload,
                           "ttl": 100,
                           "to": tos,
                           "from": froms,
                           "priority": 1
                           }
                post = web3.shh.post(options)
                return post
            return False
        except ValueError as err:
            print (err)
            return False

    '''
    Message Receiving Functions
    '''

    def get_filter_changes(self, faddr):
        print("in get filter changes")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = faddr
            getf = web3.shh.getFilterChanges(options)
            return getf
        return False

    @staticmethod
    def set_request_topic():
        print("Setting request topic")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = {"topics": [iodt_req_topic]}
            setf = web3.shh.newFilter(options)
            config.write_config("instance", "req_addr", setf)
            return setf
        return False

    @staticmethod
    def set_response_topic():
        print("Setting response topic")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = {"topics": [iodt_res_topic]}
            setf = web3.shh.newFilter(options)
            config.write_config("instance", "res_addr", setf)
            return setf
        return False

    '''
    Reply to the message
    '''

    def watch_request(self):
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        req_addr = config.config_section_map("instance")["req_addr"]
        if not req_addr:
            req_addr = self.set_request_topic()
        req = self.get_filter_changes(req_addr)
        if req:
            jreq = json.loads(req)
            for i in range(jreq["result"].__len__()):
                origin = jreq["result"][i]["from"]
                sent = jreq["result"][i]["sent"]
                dict_req.update({origin: sent})



                # check = (topic == iodt_req_topic) & (origin is not mid)   # check to exclude self
                # reply = self.post_message(iodt_res_topic, self.get_power_usage(), origin, mid)
                # return reply

    '''
    Contract Execution
    '''

    @staticmethod
    def call_contract():
        print("In contract call")
        try:
            d = cc.send('0xa6cf418b64c0c81bc70fde7e5445f513b1b4d890', '777')
            return d
        except IndexError as err:
            print(err)
            return []

    '''
    Main Worker function
    '''

    def live(self):
        print ("Setting Filters")
        t1 = self.set_request_topic()
        if t1:
            print ("Request topic set successful")
            t2 = self.set_response_topic()
            if t2:
                print ("Response topic set successful")




if __name__ == '__main__':
    pb = PowerBartering("active")
    print(pb.get_power_usage())
    # print(pb.limit_check())
    # print(pb.set_filter())
    # print(pb.get_filter_changes())
    # pb.get_peer_details("shh")
    print (pb.watch())
