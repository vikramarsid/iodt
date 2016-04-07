import time
import subprocess
from zeroconf import *
from dynamic_discovery import ServiceListener
from host_connection import HostConnect


class DynamicDiscoveryDriver(object):

    def scan(self):
        browser = ServiceBrowser(Zeroconf(), "_http._tcp.local.", ServiceListener())
        print ("Searching for devices for 40 seconds...")
        time.sleep(40)
        Zeroconf().close()

    def start_multichain_server(self):
            p = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE)
            out, err = p.communicate()
            if 'multichaind' in out:
                print('multichaind already running')
            else:
                serv = subprocess.Popen(["multichaind", "iodt-node01"], stdout=subprocess.PIPE)
                output, error = serv.communicate()
                print (output)


if __name__ == '__main__':

    scanner = DynamicDiscoveryDriver()
    connector = HostConnect()

    #scanner.start_multichain_server()

    scanner.scan()

    server = connector.connect()
    print (server.getinfo())
