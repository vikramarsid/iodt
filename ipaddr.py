import operator
import requests
import time
from multiprocessing.pool import ThreadPool

from flask import json

from config_map import ConfigMap

dict_res = {}
peer_priority = {}
config = ConfigMap()
pool = ThreadPool(processes=1)
jval = '''{
  "id":1,
  "jsonrpc":"2.0",
  "result": [{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6e8Qve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x9",
    "workProved": "0x754"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0x04e89758a62e38cd5f9f5224bedfdf9d2d629ce7f3cbfa1defbaab14eaf5743412e93983a1e4422ceee2ecffd6a20ad9b9f783ef1554ab8709f9898cae2087d26b",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x4",
    "workProved": "0x158"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0x03e89758a62e38cd5f9f5224bedfdf9d2d629ce7f3cbfa1defbaab14eaf5743412e93983a1e4422ceee2ecffd6a20ad9b9f783ef1554ab8709f9898cae2087d26b",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x2",
    "workProved": "0x589563622"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0x02e89758a62e38cd5f9f5224bedfdf9d2d629ce7f3cbfa1defbaab14eaf5743412e93983a1e4422ceee2ecffd6a20ad9b9f783ef1554ab8709f9898cae2087d26b",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "vikram",
    "sent": "vikram",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7",
    "workProved": "0x525"
    }]
}'''

class test(object):
    def get_peer_priority(self):
        print("Getting Peer priority - " + str(time.time()))
        # url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        url = "http://www.mocky.io/v2/5734bf9c1300004d03cddfaf"
        payload = {'device_id': config.config_section_map("device")['id']}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            rest = json.loads(r.text)
            print (rest["Users"][0]["email"])
            peers = rest["Devices"]
            # config.write_config("userprofile", "peercount", peers.__len__())
            for device in peers:
                peer_priority.update({device["shh_id"]: device["priority"]})
            if peer_priority.__len__() > 0:
                sorted_priority = sorted(peer_priority.items(), key=operator.itemgetter(1))
                # print (sorted_priority)
            return sorted_priority


    def retina(self):
        cost = 0
        consumption = 0
        diff = 50
        kill_nodes = []
        priority = self.get_peer_priority()
        if priority:
            jres = json.loads(jval)
            for i in range(jres["result"].__len__()):
                origin = jres["result"][i]["from"]
                res_payload = jres["result"][i]["payload"]
                dict_res.update({origin: int(res_payload, 0)})

            for values in dict_res.values():
                consumption = consumption + values

            while cost <= diff:
                org = priority.pop()[0]
                if dict_res.has_key(org):
                    cost = cost + dict_res.get(org)
                kill_nodes.append(org)

                if priority.__len__() == 1:
                    break
            print (kill_nodes)



if __name__ == '__main__':
    exe = test()
    # exe.retina()
    exe.get_peer_priority()
