import time
import subprocess
import os

from gethup import Gethup
from zeroconf import *
from dynamic_discovery import ServiceListener
current_path = os.path.dirname(os.path.realpath(__file__))


class DynamicDiscoveryDriver(object):

    def scan(self):
        browser = ServiceBrowser(Zeroconf(), "_http._tcp.local.", ServiceListener())
        print ("Searching for devices for 40 seconds...")
        time.sleep(40)
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

    #scanner = DynamicDiscoveryDriver()
    #connector = HostConnect()
    #scanner.start_blockchain_server()
    #scanner.scan()
    #server = connector.connect()
    #print (server.getinfo())
    #print current_path

    startup = Gethup()
    startup.startnode()