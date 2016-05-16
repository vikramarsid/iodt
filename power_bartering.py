# POWER BARTERING FACILITY
# 0. Initialize shh by setting the filters for topics {iodt_req_topic} {iodt_res_topic}
# 1. Start Listening for messages having {iodt_res_topic} as topic.
# 2. Start Power Bartering (Should be enabled based on the mode)
# 3. Check Usage limit
# 4. If usage is more than limit
# 5. Send broadcast message to peers, querying their usage
# 6. Start polling for changes
# 7. After receiving messages from all peers, flush the queue by shh_getMessage

import operator
import requests
import time
from multiprocessing import Process

from flask import json

import schedule
import web3_connect
from config_map import ConfigMap
from utility import Utility

config = ConfigMap()
set_web3 = web3_connect.Web3Connect()
web3 = set_web3.connect()
cc = set_web3.connect_contract()
util = Utility()

# topics
iodt_req_topic = "0x696f64745f706f7765725f626172746572696e67"
iodt_res_topic = "0x5265706c792d506f7765725573616765496e666f"
power_usage_payload = "0x73656e64506f7765725573616765"
peer_shh_ids = []
peer_contract_ids = []
dict_req = {}
dict_res = {}
peer_priority = {}

class PowerBartering:
    def __init__(self, mode):
        self.mode = mode
        self.interval = 1000
        req_filter = config.config_section_map("instance")["req_addr"]
        res_filter = config.config_section_map("instance")["res_addr"]
        if not (req_filter and res_filter):
            self.start_topics()
        p1 = Process(target=self.watch_request)
        p1.start()
        p2 = Process(target=self.watch_response)
        p2.start()
        pass

    def start_power_bartering(self):
        self.get_peer_usage("shh")
        # schedule.every(1).minutes.do(self.get_peer_usage("shh"))
        schedule.every(1).hours.do(self.get_peer_usage, "shh")
        # schedule.every(1).hour.do(self.get_peer_usage("shh"))
        while True:
            schedule.run_pending()
            time.sleep(3540)

    def get_peer_usage(self, stype):
        print("Getting Peer details - " + str(time.time()))
        #url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        url = "http://www.mocky.io/v2/5730e1fd100000ad0717f882"
        payload = {'device_id': config.config_section_map("device")['id']}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            rest = json.loads(r.text)
            peers = rest["Devices"]
            config.write_config("userprofile", "peercount", peers.__len__())
            if stype == "shh":
                for device in peers:
                    peer_shh_ids.append(device["shh_id"])
                if peer_shh_ids.__len__() > 0:
                    print ("Broadcasting Power Requirements - " + str(time.time()))
                    self.broadcast_message()

            if stype == "contract":
                for device in rest["Devices"]:
                    peer_contract_ids.append(device["contract_addr"])
                print ("Peer Contract Addresses\n" + str(peer_contract_ids))
            return rest

    @staticmethod
    def get_peer_priority():
        global sorted_priority
        print("Getting Peer priority - " + str(time.time()))
        #url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        url = "http://www.mocky.io/v2/5734bf9c1300004d03cddfaf"
        payload = {'device_id': config.config_section_map("device")['id']}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            rest = json.loads(r.text)
            peers = rest["Devices"]
            # config.write_config("userprofile", "peercount", peers.__len__())
            for device in peers:
                peer_priority.update({device["shh_id"]: device["priority"]})
            if peer_priority.__len__() > 0:
                sorted_priority = sorted(peer_priority.items(), key=operator.itemgetter(1))
                print (sorted_priority)
            return sorted_priority

    @staticmethod
    def send_kill_signal(klist):
        print("Sending kill signal - " + str(time.time()))
        # url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        url = "http://www.mocky.io/v2/5734bf9c1300004d03cddfaf"
        payload = {'kill_list': klist}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            # rest = json.loads(r.text)
            return True
        return False

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

    @staticmethod
    def get_filter_changes(faddr):
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
    def get_allmessages(faddr):
        print("in get all messages")
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        if web3.shh.hasIdentity(mid):
            options = faddr
            getf = web3.shh.getMessages(options)
            if getf:
                print("Flushed Request Queue")
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

    def start_topics(self):
        print ("Setting Filters")
        t1 = self.set_request_topic()
        if t1:
            print ("Request topic set successful")
            t2 = self.set_response_topic()
            if t2:
                print ("Response topic set successful")

    '''
    Reply to the message
    '''

    def watch_request(self):
        success = 0
        fail = 0
        mid = config.config_section_map("instance")["shh_id"]
        if mid == '':
            mid = set_web3.set_identity()
        req_addr = config.config_section_map("instance")["req_addr"]

        if not req_addr:
            req_addr = self.set_request_topic()
        peer_count = config.config_section_map("userprofile")["peercount"]

        timeout = time.time() + 60 * 2  # set time out for 5 minutes from now

        while True:
            req = self.get_filter_changes(req_addr)
            if req:
                for i in range(req.__len__()):
                    origin = req[i]["from"]
                    sent = req[i]["sent"]
                    req_payload = req[i]["payload"]
                    if req_payload == power_usage_payload:
                        dict_req.update({origin: sent})

            if dict_req.keys().__len__() == peer_count:
                break
            else:
                print ("Waiting for peer power request")

            if time.time() > timeout:
                break

        if dict_req.keys().__len__() < peer_count:
            print ("TIMEOUT:Missed messages from peers - please check power status of the peers")
        current_usage = util.get_power_usage()

        for key in dict_req.keys():
            send_res = self.post_message(iodt_res_topic, hex(current_usage), key, mid)  # Sending power usage reply
            if send_res:
                success += 1
            else:
                fail += 1

        print (
        "\nTotal messages sent to peers: " + str(dict_req.keys().__len__()) + "\nTotal successful delivery : " + str(
            success) + "\nTotal un-successful delivery: " + str(fail))

        if success > 1:
            dict_req.clear()  # clearing the dictionary
            self.get_allmessages(req_addr)  # clearing queue
            return "True"
        else:
            return "False"

    '''
    In response to the power message
    '''

    def watch_response(self):
        cost = 0
        consumption = 0
        kill_nodes = []
        priority = self.get_peer_priority
        if priority:
            mid = config.config_section_map("instance")["shh_id"]
            if mid == '':
                mid = set_web3.set_identity()
            res_addr = config.config_section_map("instance")["res_addr"]

            if not res_addr:
                res_addr = self.set_response_topic()
            peer_count = config.config_section_map("userprofile")["peercount"]

            timeout = time.time() + 60 * 2  # set time out for 5 minutes from now

            while True:
                res = self.get_filter_changes(res_addr)
                if res:
                    for i in range(res.__len__()):
                        origin = res[i]["from"]
                        res_payload = res[i]["payload"]
                        dict_res.update({origin: int(res_payload, 0)})  # Updating the response dictonary

                if dict_res.keys().__len__() == peer_count:
                    break
                else:
                    print ("Waiting for peer power resuest")

                if time.time() > timeout:
                    break

            if dict_res.keys().__len__() < peer_count:
                print ("TIMEOUT:Missed messages from peers - please check power status of the peers")

            limit = int(config.config_section_map("userprofile")['powerlimit'])

            for values in dict_res.values():
                consumption = consumption + values

            if consumption > limit:
                diff = consumption - limit

                while cost <= diff:
                    org = priority.pop()[0]
                    if dict_res.has_key(org):
                        cost = cost + dict_res.get(org)
                    kill_nodes.append(org)

                    if priority.__len__() == 1:
                        break
                print ("switching of nodes shown below:\n" + str(kill_nodes))
                kill_all = self.send_kill_signal(kill_nodes)
                if kill_all:
                    dict_res.clear()  # clearing the dictionary
                    self.get_allmessages(res_addr)  # clearing queue
                    return "True"
                else:
                    print("Couldn't send kill message to all nodes")
                    return "False"
            return True

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

if __name__ == '__main__':
    pb = PowerBartering("active")
    print(pb.start_power_bartering())
    # print(pb.limit_check())
    # print(pb.set_filter())
    # print(pb.get_filter_changes())
    # pb.get_peer_details("shh")
    # print (pb.watch())
