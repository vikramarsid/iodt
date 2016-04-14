import requests
import json
from zeroconf import *
import socket


class ServiceListener(object):
    def __init__(self):
        self.r = Zeroconf()

    def removeService(self, zeroconf, type, name):
        print
        print "Service", name, "removed"

    def addService(self, zeroconf, type, name):
        print
        print "Service", name, "added"
        print "  Type is", type
        info = self.r.getServiceInfo(type, name)
        if info:
            ipaddrs = socket.inet_ntoa(info.getAddress())
            portaddr = info.getPort()
            enodeurl = self.curl_url()
            print "  Address is %s:%d" % (ipaddrs, portaddr)
            print "enode url %s" % (enodeurl)
            print "  Weight is %d, Priority is %d" % (info.getWeight(), info.getPriority())
            print "  Server is", info.getServer()
            prop = info.getProperties()
            if prop:
                print "  Properties are"
                for key, value in prop.items():
                    print "    %s: %s" % (key, value)
            return ipaddrs
