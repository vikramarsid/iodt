from multiprocessing.pool import ThreadPool

from flask import json

from config_map import ConfigMap

com = {}
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
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6eW8ve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6Ae8ve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18vS6e8ve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "vikram",
    "sent": "vikram",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    }]
}'''

class test(object):


    def retina(self):
        jres = json.loads(jval)
        for i in range(jres["result"].__len__()):
            origin = jres["result"][i]["from"]
            sent = jres["result"][i]["sent"]
            com.update({origin: sent})

        for key in com.keys():
            print (key)



if __name__ == '__main__':
    exe = test()
    exe.retina()
