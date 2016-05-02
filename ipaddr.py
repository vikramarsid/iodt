import re
import requests
import  subprocess
from multiprocessing.pool import ThreadPool

from eth_ipc_client import Client
from flask import json

from config_map import ConfigMap

config = ConfigMap()

pool = ThreadPool(processes=1)

client = Client("/home/ubuntu/iodt-node/data/03/geth.ipc")


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
    exe = test()
    # print client.get_code("0x4130774716a6ad06af7cbe5585b5139710135efc", block="latest")
    print client.get_transaction_by_hash("0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421")
    print client.get_block_by_number("0x38f388fadf4a6a35c61c3f88194ec5ae162c8944")
