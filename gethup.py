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
from shutil import *

from flask import json

import web3_connect
from config_map import ConfigMap
from feeder import Feeder
from power_bartering import PowerBartering

config = ConfigMap()
pool = ThreadPool(processes=1)
set_web3 = web3_connect.Web3Connect()
upload_data = Feeder()


class Gethup(object):
    # start up initials
    device_id = config.config_section_map("device")['id']
    device_name = config.config_section_map("device")['name']
    instance_id = config.config_section_map("instance")['id']
    server_url = config.config_section_map("server")['url'] + 'devices'
    shh_id = config.config_section_map("instance")['shh_id']
    network_id = config.config_section_map("instance")['network_id']
    port = config.config_section_map("instance")['port']
    c_addr = config.config_section_map("instance")['contract_address']
    status = config.config_section_map("device")['status']
    directory = expanduser("~") + "/iodt-node"
    device_power_level = PowerBartering(status).get_power_usage()

    # geth CLI params
    datetag = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
    datadir = directory + '/data/' + instance_id
    log = directory + '/log/' + instance_id + '.' + datetag + '.log'
    linklog = directory + '/log/' + instance_id + '.current.log'
    stablelog = directory + '/log/' + instance_id + '.log'
    keystore = directory + '/keystore/' + instance_id
    password = instance_id
    rpcport = '82' + instance_id
    enodeid = ''
    accno = ''

    @staticmethod
    def get_ip_address():
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        return ipaddr

    def ext_curl(self):
        url = self.server_url
        payload = {'enode': self.enodeid, 'host': self.get_ip_address(), 'rpcport': self.rpcport, 'port': self.port,
                   'device_id': self.device_id, 'account': self.accno, 'name': self.device_name, 'status': self.status,
                   'network_id': self.network_id, 'shh_id': self.shh_id, 'contract_addr': self.c_addr,
                   'power_usage': self.device_power_level,
                   'id': str(int(time.time()))}

        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            print("Global Call: " + r.text)
            rest = json.loads(r.text)
            # config.write_power_profile(rest["power_usage"], rest["id"])  # setting powerlimit and priority
            aync_call = pool.apply_async(upload_data.run)
        return r.text

    def local_curl(self, strs):
        config.write_config("instance", "account", self.accno)
        shh_id = set_web3.set_identity()  # setting shh_id
        if shh_id:
            print ("==========shh_id===============\n" + shh_id)

        local_url = "http://localhost:" + self.rpcport
        payload = '{"jsonrpc": "2.0", "method": "admin_nodeInfo", "params": [], "id": 74}'
        r = requests.post(local_url, data=payload)
        d = json.loads(r.text)
        print(d["result"]["enode"])
        if r.status_code == 200:
            self.enodeid = d["result"]["id"]
            # print ("------------------" + d["result"]["enode"])
            config.write_config("instance", "enode", self.enodeid)
            print ("pushing to CMS------")
            self.ext_curl()
        return self.enodeid

    def execute(self, cmd, *args, **kwargs):
        print ("---executing command : " + cmd)
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
            print (line)

            if line == '' and not p.poll():
                break

        p.wait()
        p.communicate()
        return {"ret": p.returncode, "val": ''.join(stdout), "found": found}

    @staticmethod
    def mkdir(path):

        try:
            if not os.path.exists(path):
                os.makedirs(path)
                print ("---Directory create--- " + path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    @staticmethod
    def copy(src, dst):

        try:
            print ("---Copying--- \n" + src + " to " + dst)
            copytree(src, dst)

        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    def givegeth(self, curaccno):
        geth_cmd = 'geth' + \
                   ' --identity "' + self.device_name + '"' \
                                                        ' --networkid ' + self.network_id + \
                   ' --genesis ./genesis.json' + \
                   ' --datadir ' + self.datadir + \
                   ' --unlock ' + curaccno + \
                   ' --password <(echo -n ' + self.instance_id + ')' + \
                   ' --port ' + self.port + \
                   ' --rpc' + \
                   ' --rpcaddr 0.0.0.0' + \
                   ' --rpcport ' + self.rpcport + \
                   ' --rpccorsdomain "*"' + \
                   ' --rpcapi "admin,db,eth,net,web3,shh"' + \
                   ' --nodiscover' + \
                   ' --autodag=false' + \
                   ' --fast' + \
                   ' --shh' + \
                   ' --lightkdf' + \
                   ' --dev' + \
                   ' --verbosity="5"' + \
                   ' --maxpeers 50' + \
                   ' js ./mine.js'

        return geth_cmd

    def startnode(self):

        # start up initials

        directory = self.directory
        instance_id = self.instance_id
        # datetag = self.datetag
        datadir = self.datadir
        log = self.log
        linklog = self.linklog
        # stablelog = self.stablelog
        keystore = self.keystore
        # password = self.password
        # port = self.port
        # rpcport = self.rpcport
        # network_id = self.network_id

        # bash commands

        account_cmd = 'geth' + \
                      ' --datadir=' + datadir + \
                      ' account list|head -n1|perl -ne "/([a-f0-9]{40})/ && print $1"'

        create_acc = 'geth' + \
                     ' --datadir ' + datadir + \
                     ' --password <(echo -n ' + instance_id + ') account new'

        # create main directory
        print (directory)
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
            print ("Copying keystore")
            self.copy(datadir + '/keystore', keystore)

        if not os.path.exists(datadir + '/keystore'):
            print ("Copying keys")
            self.copy(keystore + '/keystore', datadir + '/keystore')

        account_no = self.execute(account_cmd)
        logno = str(account_no["val"])
        # temp = logno.find("{")
        self.accno = logno[logno.find("{") + 1:logno.find("}")]
        print ("account_no-----\n" + self.accno)

        if self.accno != '':
            print (self.accno)
            geth_command = self.givegeth(self.accno)
            # final_run = self.execute(geth_command, param="IPC service started")
            final_run = self.execute(geth_command, param="IPC endpoint opened")
            print ("geth-----\n" + str(final_run["val"]))
