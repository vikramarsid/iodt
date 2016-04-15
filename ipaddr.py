import re
import requests
import  subprocess
from multiprocessing.pool import ThreadPool

from flask import json

from config_map import ConfigMap

config = ConfigMap()

pool = ThreadPool(processes=1)

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


if __name__ == '__main__':
    # exe = test()
    #print "device_id: " + config.ConfigSectionMap("instance")['id']
    #print "device_name: " + config.ConfigSectionMap("device")['name']

    # ff = exe.execute('geth --identity "iodtg-node01" --genesis /home/ubuntu/Desktop/iodt_genesis.json --rpc --rpcport "8080" --rpccorsdomain "*" --datadir "/home/ubuntu/iodt01" --port "30301" --nodiscover --rpcapi "admin,db,eth,net,web3" --networkid 2007',param="IPC service started")
    # print "============================\n" + str(ff["found"]) + "============================\n" + str(ff["ret"]) + "============================\n" + str(ff["val"])


    payload = {'enode': 'self.enodeid', 'host': 'self.get_ip_address()', 'rpcport': 'self.rpcport', 'port': 'self.port',
               'dev-id': 'self.device_id', 'dev-name': 'self.device_name', 'id': 'str(randint(0, 1000))'}

    print json.dumps(payload)
