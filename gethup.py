import datetime
import errno
import os
import re
import requests
import socket
import subprocess
import time
from multiprocessing.pool import ThreadPool
from os.path import expanduser
from random import randint
from shutil import *

from flask import json

from config_map import ConfigMap

config = ConfigMap()
pool = ThreadPool(processes=1)


class Gethup(object):
    # start up initials
    device_id = config.ConfigSectionMap("device")['id']
    device_name = config.ConfigSectionMap("device")['name']
    instance_id = config.ConfigSectionMap("instance")['id']
    directory = expanduser("~") + "/iodt-node"

    # geth CLI params
    datetag = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
    datadir = directory + '/data/' + instance_id
    log = directory + '/log/' + instance_id + '.' + datetag + '.log'
    linklog = directory + '/log/' + instance_id + '.current.log'
    stablelog = directory + '/log/' + instance_id + '.log'
    keystore = directory + '/keystore/' + instance_id
    password = instance_id
    port = '311' + instance_id
    rpcport = '82' + instance_id
    network_id = '9030'
    enodeid = ''

    def get_ip_address(self):
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        return ipaddr

    def ext_curl(self):
        url = "http://iodt.herokuapp.com/api/bootdevices"
        payload = {'enode': self.enodeid, 'host': self.get_ip_address(), 'rpcport': self.rpcport, 'port': self.port,
                   'dev-id': self.device_id, 'dev-name': self.device_name, 'id': str(randint(0, 1000))}

        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            print "Global Call: " + r.text
        return r.text

    def local_curl(self, strs):
        localURL = "http://localhost:" + self.rpcport
        payload = '{"jsonrpc": "2.0", "method": "admin_nodeInfo", "params": [], "id": 74}'
        r = requests.post(localURL, data=payload)
        d = json.loads(r.text)
        print d["result"]["enode"]
        if (r.status_code == 200):
            self.enodeid = d["result"]["id"]
            print "------------------" + d["result"]["enode"]
            print "pushing to CMS------"
            self.ext_curl()
        return self.enodeid

    def execute(self, cmd, *args, **kwargs):
        print "---executing command : " + cmd
        found = ''
        stdout = []
        p = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            if 'param' in kwargs:
                param = kwargs['param']
                m = re.search(param, line)
                if m:
                    found = m.string[m.string.find(param):len(m.string)]
                    async_result = pool.apply_async(self.local_curl(found))
            print line

            if line == '' and p.poll() != None:
                break

        p.wait()
        p.communicate()
        return {"ret": p.returncode, "val": ''.join(stdout), "found": found}

    def mkdir(self, path):

        try:
            if not os.path.exists(path):
                os.makedirs(path)
                print "---Directory create--- " + path
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def copy(self, src, dst):

        try:
            print "---Copying--- \n" + src + " to " + dst
            copytree(src, dst)

        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    def startnode(self):

        # start up initials

        directory = self.directory
        instance_id = self.instance_id
        datetag = self.datetag
        datadir = self.datadir
        log = self.log
        linklog = self.linklog
        stablelog = self.stablelog
        keystore = self.keystore
        password = self.password
        port = self.port
        rpcport = self.rpcport
        network_id = self.network_id

        # bash commands
        geth_cmd = 'geth' + \
                   ' --identity "' + self.device_name + '"' \
                                                        ' --networkid ' + network_id + \
                   ' --genesis ./genesis.json' + \
                   ' --datadir ' + datadir + \
                   ' --rpc' + \
                   ' --rpcport ' + rpcport + \
                   ' --rpccorsdomain "*"' + \
                   ' --rpcapi "admin,db,eth,net,web3"' + \
                   ' --nodiscover' + \
                   ' --fast' + \
                   ' --shh' + \
                   ' --lightkdf'

        account_cmd = 'geth' + \
                      ' --datadir=' + datadir + \
                      ' account list|head -n1|perl -ne "/([a-f0-9]{40})/ && print $1"'

        create_acc = 'geth' + \
                     ' --datadir ' + datadir + \
                     ' --password <(echo -n ' + instance_id + ') account new'

        # create main directory
        print directory
        self.mkdir(directory)
        self.mkdir(directory + '/data/')
        self.mkdir(directory + '/log/')
        try:

            os.symlink(log, linklog)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

        # create ethereum account if not created
        if not os.path.exists(keystore):
            self.mkdir(keystore)
        acc_status = self.execute(str(create_acc))
        if acc_status["ret"] == 0:
            print "Copying keystore"
            self.copy(datadir + '/keystore', keystore)

        if not os.path.exists(datadir + '/keystore'):
            print "Copying keys"
            self.copy(keystore + '/keystore', datadir + '/keystore')

        account_no = self.execute(account_cmd)
        print "account_no-----\n" + str(account_no["val"])

        final_run = self.execute(geth_cmd,param="IPC service started")
        print "geth-----\n" + str(final_run["val"])
