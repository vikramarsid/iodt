import os
import socket
import subprocess


class Utility(object):
    @staticmethod
    def get_ip_address():
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        return ipaddr

    @staticmethod
    def get_power_usage():
        command = "upower -i $(upower -e | grep BAT) | grep --color=never -E percentage|xargs|cut -d' ' -f2|sed s/%//"
        get_battery_data = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
        val = get_battery_data.communicate()[0].decode("utf-8").replace("\n", "")
        return val
