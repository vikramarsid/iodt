import socket

from config_map import ConfigMap
from zeroconf import *

config = ConfigMap()


class ServiceListener(object):
    def __init__(self):
        self.r = Zeroconf()

    def removeService(self, zeroconf, type, name):
        print ("Service " + name + "removed")

    def addService(self, zeroconf, type, name):
        print ("Service " + name + " added")
        print ("  Type is " + type)
        info = self.r.getServiceInfo(type, name)
        if info:
            ipaddrs = socket.inet_ntoa(info.getAddress())
            portaddr = info.getPort()
            addr = str(ipaddrs) + ":7000/api/"
            print ("  Address is " + addr)
            print ("  Weight is " + str(info.getWeight()) + ", Priority is " + str(info.getPriority()))
            print ("  Server is" + str(info.getServer()))
            prop = info.getProperties()
            if prop:
                print ("  Properties are\n")
                for key, value in prop.items():
                    print (key + ":" + value)
            config.write_config("server", "url", "http://" + addr)
            return addr
