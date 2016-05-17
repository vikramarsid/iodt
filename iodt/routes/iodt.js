
var express = require('express');
var router = express.Router();
var mysql = require("mysql");

var mySQLHelper = require('../helper/mySQLHelper');
var web3Helper = require('../helper/web3Helper');
var stringUtils = require('../helper/stringUtils');

var fs = require("fs");
var Converter = require("csvtojson").Converter;
var converter = new Converter({});
var csvFileName = "./pge.csv";
var pgeJson;
converter.on("end_parsed",function(jsonObj) {
	pgeJson = jsonObj;
});
fs.createReadStream(csvFileName).pipe(converter);


/* GET all unassigned devices listing */
router.get('/availableDevices', function(req, res) {

	var query = "SELECT * FROM devices WHERE devices.device_id NOT IN (SELECT iodt.device_id FROM iodt WHERE iodt.device_id IS NOT NULL)";
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No Devices Found."});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
		}

	}).bind(params));

});


/* POST method to add devices to cluster */
/* PARAMS user_name, cluster_id */
/* BODY device_id */
router.post('/addDevices/user/:user_name/cluster/:cluster_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.user_name) || stringUtils.isEmpty(req.params.cluster_id) || req.body.device_id.length == 0) {
		return res.json({"Error" : true, "Message" : "All values are mandatory"});
	}

	var query = "SELECT * FROM devices WHERE device_id IN (SELECT device_id FROM iodt WHERE cluster_id = ?) LIMIT 1";
	var values = [req.params.cluster_id];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else {

			this.rows = rows;
			if(typeof this.req.body.device_id != "object") {
				this.req.body.device_id = [this.req.body.device_id];
			}

			var query = "SELECT * FROM devices WHERE device_id IN (?)";
			var values = [this.req.body.device_id];
			query = mysql.format(query, values);

			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else  {

					var count = 0;
					var totalDevices = this.req.body.device_id.length;

					try {
						// var web3Obj = web3Helper.createWeb3(this.rows[0].host, this.rows[0].rpcport);
						for (var i = 0; i < this.req.body.device_id.length; i++) {
							var peerAddress = "enode://" + rows[i].enode + "@" + rows[i].host + ":" + rows[i].port;
							// web3Obj.admin.addPeer(peerAddress);

							var query = "INSERT INTO iodt (user_name, cluster_id, device_id, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW())";
							var values = [this.req.params.user_name, this.req.params.cluster_id, this.req.body.device_id[i]];
							query = mysql.format(query, values);
							mySQLHelper.executeSQLQuery(query, (function(err, rows) {
								count++;
								if(err) {
									return this.res.json({"Error" : true, "Message" : err});
								} else if(rows.length > 0) {
									return this.res.json({"Error" : false, "Message" : "Error in adding device. Please try again."});
								} else {
									if(count == totalDevices) {

										var query = "SELECT * FROM devices WHERE device_id IN (?)";
										var values = [this.req.body.device_id];
										query = mysql.format(query, values);
										console.log(query);
										mySQLHelper.executeSQLQuery(query, (function(err, rows) {

											if(err) {
												return this.res.json({"Error" : true, "Message" : err});
											} else if(rows.length == 0) {
												return this.res.json({"Error" : false, "Message" : "Device with device ID '" + this.req.params.device_id + "' is not present"});
											} else if(rows.length > 0) {
												return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
											}

										}).bind(this));
									}
								}

							}).bind(this));
						}

					} catch(err) {
						return this.res.json({"Error" : false, "Message" : "Error while creating new cluster. Please try again."});
					}

				}

			}).bind(this));

		}

	}).bind(params));

});


/* DELETE removes a device from cluster */
/* PARAMS user_name, cluster_id, device_id */
router.delete('/removeDevices/user/:user_name/cluster/:cluster_id/device/:device_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.cluster_id)) {
		return res.json({"Error" : false, "Message" : "No cluster_id specified"});
	}

	var query = "DELETE FROM iodt WHERE device_id = ?";
	var values = [req.params.device_id];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}

	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "Error in removing a device from cluster. Please try again."});
		} else if(rows.affectedRows > 0) {
			return this.res.json({"Error" : false, "Message" : "Success"});
		}

	}).bind(params));

});


/* GET all unassigned devices listing */
router.post('/peerinfo', function(req, res) {

	if(stringUtils.isEmpty(req.body.device_id)) {
		return res.json({"Error" : false, "Message" : "No device_id specified"});
	}

	var query = "SELECT * FROM iodt WHERE device_id = ?";
	var values = [req.body.device_id];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No Devices Found."});
		} else if(rows.length > 0) {

			var response = {"Error" : false, "Message" : "Success"};

			var query = "SELECT device_id, enode, host, port, rpcport, contract_addr, shh_id, account, priority FROM devices WHERE device_id NOT IN (?) AND device_id IN (SELECT device_id FROM iodt WHERE cluster_id = ?)";
			var values = [this.req.body.device_id, rows[0].cluster_id];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {
					return this.res.json({"Error" : false, "Message" : "No Devices Present"});
				} else if(rows.length > 0) {
					buildResponse("Devices", this, rows);
				}

			}).bind(this));


			var query = "SELECT cluster_id, power_limit FROM clusters WHERE cluster_id = ?";
			var values = [rows[0].cluster_id];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {
					return this.res.json({"Error" : false, "Message" : "No Devices Present"});
				} else if(rows.length > 0) {
					buildResponse("Clusters", this, rows);
				}

			}).bind(this));


			var query = "SELECT email, user_name FROM users WHERE user_name = ?";
			var values = [rows[0].user_name];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else {
					buildResponse("Users", this, rows);
				}

			}).bind(this));

			function buildResponse(type, that, rows) {
				if(type == "Users") {
					response["Users"] = rows;
				} else if(type == "Clusters") {
					response["Clusters"] = rows;
				} else if(type == "Devices") {
					response["Devices"] = rows;
				}
				if(("Devices" in response) && ("Clusters" in response) && ("Users" in response)) {
					console.log(response);
					return that.res.json(response);
				}
			}

		}

	}).bind(params));

});


/* GET power usage */
router.get('/powerusage', function(req, res) {

	res.json(pgeJson);

});


module.exports = router;
