import re
import requests
import  subprocess
from multiprocessing.pool import ThreadPool

from flask import json

from config_map import ConfigMap

com = {}
config = ConfigMap()
pool = ThreadPool(processes=1)
# ipcpath = expanduser("~") + "/iodt-node" + '/data/' + config.config_section_map("instance")['id'] + '/geth.ipc'
# web3 = Web3(IPCProvider(ipcpath, testnet=False))
# web3.config.defaultAccount = config.config_section_map("instance")["account"]
# web3.config.defaultBlock = "latest"
jval = '''{
  "id":1,
  "jsonrpc":"2.0",
  "result": [{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6e8ve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6e8ve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6e8ve68ve84v",
    "to": "0x87gdf76g8d7fgdfg...",
    "expiry": "0x54caa50a",
    "sent": "0x54ca9ea2",
    "ttl": "0x64",
    "topics": ["0x6578616d"],
    "payload": "0x7b2274797065223a226d657373616765222c2263686...",
    "workProved": "0x0"
    },{
    "hash": "0x33eb2da77bf3527e28f8bf493650b1879b08c4f2a362beae4ba2f71bafcd91f9",
    "from": "0xe18v6e8ve68ve84v",
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

    def curl_url(self,strs):
        finalURL = "http://localhost:8080"
        payload = '{"jsonrpc": "2.0", "method": "admin_nodeInfo", "params": [], "id": 74}'
        enode_url = None
        r = requests.post(finalURL, data=payload)
        d = json.loads(r.text)
        print d["result"]["enode"]
        if (r.status_code == 200):
            enode_url = d["result"]["enode"]
            print "------------------" + d["result"]["enode"]
        return enode_url

    def show(self, res):
        print res


    def execute(self,cmd, *args, **kwargs):
        print "---executing command : " + cmd
        found = ''
        stdout = []

        if 'param' in kwargs:
            param = kwargs['param']

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            m = re.search(param, line)
            if m:
                found = m.string[m.string.find(param):len(m.string)]
                async_result = pool.apply_async(self.curl_url(found))
            print line

            if line == '' and p.poll() != None:
                break

        p.wait()
        p.communicate()
        return {"ret": p.returncode, "val": ''.join(stdout), "found": found}

    def retina(self):
        jres = json.loads(jval)
        for i in range(jres["result"].__len__()):
            origin = jres["result"][i]["from"]
            sent = jres["result"][i]["sent"]
            com.update({origin: sent})
        print com.viewitems()
        print com.get("0xv31r53er18ve138v1e3rve1ve.")



if __name__ == '__main__':
    exe = test()
    # myIdentity = web3.shh.newIdentity()
    # r = web3.shh.filter({"topic":["0x68656c6c6f20776f726c64"]})
    # q = web3.shh.post({"topics": "power_msg","payload": "Hi this is test message","priority": "0x64","ttl": "0x64"})
    # print r
    # print q
    #print web3.shh.getFilterChanges("0x7")
    # print client.get_code("0x4130774716a6ad06af7cbe5585b5139710135efc", block="latest")
    # print client.get_transaction_by_hash("0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421")
    #print client.get_block_by_number("0x38f388fadf4a6a35c61c3f88194ec5ae162c8944")
    exe.retina()
