import socket
import jsonrpclib
import os
from read_credentials import ReadBlockCredentials


class HostConnect(object):

    def get_ip_address(ifname):
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        return ipaddr

    def connect(self):
        conparam = ReadBlockCredentials()
        ipaddr = self.get_ip_address()
        username = conparam.username().replace("\n", "")
        password = conparam.password().replace("\n", "")
        print ('http://'+username+':'+password+'@localhost:6736')
        server = jsonrpclib.Server('http://'+username+':'+password+'@localhost:6736')
        return server
