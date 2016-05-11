import requests
import time

from flask import json

from config_map import ConfigMap

config = ConfigMap()


class GetUserProfile(object):
    def __init__(self):
        pass

    @staticmethod
    def get_user():
        print("Sending email details - " + str(time.time()))
        url = config.config_section_map("server")['url'] + 'iodt/peerinfo'
        payload = {'device_id': config.config_section_map("device")['id']}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code == 200:
            rest = json.loads(r.text)
