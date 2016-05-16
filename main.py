import os
import subprocess
import time

from dynamic_discovery import ServiceListener
from gethup import Gethup
from zeroconf import *

current_path = os.path.dirname(os.path.realpath(__file__))


class DynamicDiscoveryDriver(object):

    def scan(self):
        browser = ServiceBrowser(Zeroconf(), "_http._tcp.local.", ServiceListener())
        print ("Searching for devices for 10 seconds...")
        time.sleep(10)
        Zeroconf().close()


    def start_blockchain_server(self):
            p = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE)
            out, err = p.communicate()
            if 'geth' in out:
                print('Ethereum client is already running')
            else:
                serv = subprocess.Popen(['bash', 'gethup.sh'], stdout=subprocess.PIPE).wait()
                output, error = serv.communicate()
                print (output)


if __name__ == '__main__':
    scanner = DynamicDiscoveryDriver()
    scanner.scan()
    startup = Gethup()
    startup.startnode()