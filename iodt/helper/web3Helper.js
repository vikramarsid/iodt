
var web3 = require('web3');
var web3_extended = require('web3_extended');

var web3Helper = {};

web3Helper.options = {
	host: 'http://',
	admin: true,
	debug: false,
	db: true,
	eth: true,
	net: true,
	personal: true, 
	shh: true,
	watches: true,
};


web3Helper.createWeb3 = function(host, port) {
	web3Helper.options.host += host + ":" + port;
	return web3_extended.create(web3Helper.options);
}


module.exports = web3Helper;
