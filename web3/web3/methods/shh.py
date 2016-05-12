import web3.web3.formatters as formatters
from web3.web3.method import Method

methods = [
    {
        "name": "post",
        "call": "shh_post",
        "params": 1,
        "inputFormatter": [formatters.inputPostFormatter]
    },
    {
        "name": "newIdentity",
        "call": "shh_newIdentity",
        "params": 0
    },
    {
        "name": "hasIdentity",
        "call": "shh_hasIdentity",
        "params": 1
    },
    {
        "name": "newFilter",
        "call": "shh_newFilter",
        "params": 1
    },
    {
        "name": "getFilterChanges",
        "call": "shh_getFilterChanges",
        "params": 1
    },
    {
        "name": "getMessages",
        "call": "shh_getMessages",
        "params": 0
    },
    {
        "name": "newGroup",
        "call": "shh_newGroup",
        "params": 0
    },
    {
        "name": "addToGroup",
        "call": "shh_addToGroup",
        "params": 0
    }
]


class Shh(object):
    def __init__(self, web3):
        self._requestManager = web3._requestManager

        for method in methods:
            method = Method(method)
            method.attachToObject(self)
            method.setRequestManager(web3._requestManager)
