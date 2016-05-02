var fs = require('fs');
var ini = require('ini');

var config = ini.parse(fs.readFileSync('./device.config', 'utf-8'));

module.exports = {
    build: {},
    deploy: [
        "NodeManagement"
    ],
    rpc: {
        host: "localhost",
        port: config.device.rpcport
    }
};
