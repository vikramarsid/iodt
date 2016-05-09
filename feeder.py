import os
import requests
import socket
import time
from os.path import expanduser

from flask import json

import schedule
from config_map import ConfigMap
from power_bartering import PowerBartering

config = ConfigMap()
from web3_connect import Web3Connect

set_web3 = Web3Connect()

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
rpcport = '82' + instance_id
enode = config.config_section_map("instance")['enode']
accno = config.config_section_map("instance")['account']


class Feeder(object):
    """ The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        # """ Constructor
        # :type interval: int
        # :param interval: Check interval, in seconds
        # """
        self.interval = interval
        # thread = threading.Thread(target=self.run, args=())
        # thread.daemon = True                            # Daemonize thread
        # thread.start()                                  # Start the execution

    def get_ip_address(self):
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        return ipaddr

    def job(self):
        print("Updating Central Database - " + str(time.time()))
        url = server_url
        shh_id = set_web3.set_identity()  # setting shh_id
        payload = {'enode': enode, 'host': self.get_ip_address(), 'rpcport': rpcport, 'port': port,
                   'device_id': device_id, 'account': accno, 'name': device_name, 'status': status,
                   'network_id': network_id, 'shh_id': shh_id, 'contract_addr': c_addr,
                   'power_usage': device_power_level,
                   'id': str(int(time.time()))}

        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            print "Global Call: " + r.text
            rest = json.loads(r.text)
            config.write_power_profile(rest["power_usage"], rest["id"])  # setting powerlimit and priority
        return r.text

    def run(self):
        print('Doing something imporant in the background')
        schedule.every(0.1).minutes.do(self.job)
        # schedule.every().hour.do(self.job)
        # schedule.every().day.at("10:30").do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)

            # example = Feeder()
            # example.run()
