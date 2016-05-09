
var express = require('express');
var router = express.Router();
var mysql = require("mysql");

var mySQLHelper = require('../helper/mySQLHelper');
var stringUtils = require('../helper/stringUtils');


/* GET all devices listing */
router.get('/', function(req, res) {

	var query = "SELECT * FROM devices";
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No devices present."});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
		}

	}).bind(params));

});


/* GET device by device_id */
/* PARAMS device_id */
router.get('/:device_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.device_id)) {
		return res.json({"Error" : false, "Message" : "No device_id specified"});
	}

	var query = "SELECT * FROM devices WHERE device_id = ?";
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
			return this.res.json({"Error" : false, "Message" : "Device with device ID '" + this.req.params.device_id + "' is not present"});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
		}

	}).bind(params));

});


/* GET all devices for user_name */
/* PARAMS user_name */
router.get('/user/:user_name', function(req, res) {

	if(stringUtils.isEmpty(req.params.user_name)) {
		return res.json({"Error" : false, "Message" : "No user_name specified"});
	}

	var query = "SELECT device_id FROM iodt WHERE user_name = ?";
	var values = [req.params.user_name];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No devices present for user name '" + this.req.params.user_name + "'"});
		} else if(rows.length > 0) {

			var device_id_array = [];
			for(var row in rows) {
				device_id_array.push(rows[row].device_id);
			}
			var query = "SELECT * FROM devices WHERE device_id IN (?)";
			var values = [device_id_array];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {
					return this.res.json({"Error" : false, "Message" : "No devices present for user name '" + this.req.params.user_name + "'"});
				} else if(rows.length > 0) {
					return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
				}

			}).bind(this));
		}

	}).bind(params));

});


/* GET all devices for cluster_id */
/* PARAMS cluster_id */
router.get('/cluster/:cluster_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.cluster_id)) {
		return res.json({"Error" : false, "Message" : "No cluster_id specified"});
	}

	var query = "SELECT device_id FROM iodt WHERE cluster_id = ?";
	var values = [req.params.cluster_id];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No devices present for cluster id '" + this.req.params.cluster_id + "'"});
		} else if(rows.length > 0) {

			var device_id_array = [];
			for(var row in rows) {
				device_id_array.push(rows[row].device_id);
			}
			var query = "SELECT * FROM devices WHERE device_id IN (?)";
			var values = [device_id_array];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {
					return this.res.json({"Error" : false, "Message" : "No devices present for cluster id '" + this.req.params.cluster_id + "'"});
				} else if(rows.length > 0) {
					return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
				}

			}).bind(this));
		}

	}).bind(params));

});


/* POST create device */
/* PARAMS ?????????????????????????????????????????????????????????????? */
/* BODY name, enode, host, description, power_usage, priority, status */
router.post('/', function(req, res) {

	if(stringUtils.isEmpty(req.body.device_id)) {
		return res.json({"Error" : true, "Message" : "All values are mandatory"});
	}

	var query = "SELECT * FROM devices WHERE device_id = ?";
	var values = [req.body.device_id];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length > 0) {

			var query = "UPDATE devices SET enode = ?, host = ?, port = ?, rpcport = ?, account = ?, contract_addr = ?, network_id = ?, shh_id = ?, power_usage = ?, updated_at = NOW() WHERE  device_id = ?";
			var values = [this.req.body.enode, this.req.body.host, this.req.body.port, this.req.body.rpcport, this.req.body.account, this.req.body.contract_addr, this.req.body.network_id, this.req.body.shh_id, this.req.body.power_usage, this.req.body.device_id];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.affectedRows == 0) {
					return this.res.json({"Error" : false, "Message" : "Error while updating existing device. Please try again."});
				} else if(rows.affectedRows > 0) {

					var query = "SELECT * FROM devices WHERE device_id = ?";
					var values = [this.req.body.device_id];
					query = mysql.format(query, values);
					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "No device found with id '" + this.req.params.device_id + "'"});
						} else if(rows.length > 0) {
							return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
						}

					}).bind(this));
				}

			}).bind(this));


		} else if(rows.length == 0) {

			var query = "INSERT INTO devices (id, device_id, name, enode, host, port, rpcport, account, contract_addr, network_id, shh_id, description, power_usage, priority, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW())";
			var values = [req.body.id, req.body.device_id, req.body.name, req.body.enode, req.body.host, req.body.port, req.body.rpcport, req.body.account, req.body.contract_addr, req.body.network_id, req.body.shh_id, req.body.description, req.body.power_usage, req.body.priority, req.body.status];
			query = mysql.format(query, values);

			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.affectedRows == 0) {
					return this.res.json({"Error" : false, "Message" : "Error while creating new device. Please try again."});
				} else if(rows.affectedRows > 0) {

					var query = "SELECT * FROM devices WHERE device_id = ?";
					var values = [this.req.body.device_id];
					query = mysql.format(query, values);
					console.log(query);
					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "No device found. Please try again."});
						} else if(rows.length > 0) {
							return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
						}

					}).bind(this));
				}

			}).bind(this));
		}

	}).bind(params));


});


/* PUT update device */
/* PARAMS device_id */
/* BODY name, enode, host, description, power_usage, priority, status */
router.put('/:device_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.device_id) || stringUtils.isEmpty(req.body.name) || stringUtils.isEmpty(req.body.enode) || stringUtils.isEmpty(req.body.host) || stringUtils.isEmpty(req.body.description) || stringUtils.isEmpty(req.body.power_usage) || stringUtils.isEmpty(req.body.priority) || stringUtils.isEmpty(req.body.status)) {
		return res.json({"Error" : true, "Message" : "No name, enode, host or description given to a device"});
	}

	var query = "SELECT * FROM devices WHERE device_id = ?";
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
			return this.res.json({"Error" : false, "Message" : "Device with device id '" + this.req.params.device_id + "' is not present"});
		} else if(rows.length > 0) {

			var query = "UPDATE devices SET name = ?, enode = ?, host = ?, description = ?, power_usage = ?, priority = ?, status = ?, updated_at = NOW() WHERE device_id = ?";
			var values = [this.req.body.name, this.req.body.enode, this.req.body.host, this.req.body.description, this.req.body.power_usage, this.req.body.priority, this.req.body.status, this.req.params.device_id];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.affectedRows == 0) {
					return this.res.json({"Error" : false, "Message" : "Error while updating existing device. Please try again."});
				} else if(rows.affectedRows > 0) {

					var query = "SELECT * FROM devices WHERE device_id = ?";
					var values = [this.req.params.device_id];
					query = mysql.format(query, values);
					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "No device found with id '" + this.req.params.device_id + "'"});
						} else if(rows.length > 0) {
							return this.res.json({"Error" : false, "Message" : "Success", "Devices" : rows});
						}

					}).bind(this));
				}

			}).bind(this));
		}

	}).bind(params));

});


/* DELETE device by device_id */
/* PARAMS device_id */
router.delete('/:device_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.device_id)) {
		return res.json({"Error" : false, "Message" : "No device_id specified"});
	}

	var query = "SELECT * FROM devices WHERE device_id = ?";
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
			return this.res.json({"Error" : false, "Message" : "Device with device id '" + this.req.params.device_id + "' is not present"});
		} else if(rows.length > 0) {

			var query = "SELECT device_id FROM iodt WHERE device_id = ?";
			var values = [this.req.params.device_id];
			query = mysql.format(query, values);

			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {

					var query = "DELETE FROM devices WHERE device_id = ?";
					var values = [this.req.params.device_id];
					query = mysql.format(query, values);

					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "Error in deleteing existing device. Please try again."});
						} else if(rows.affectedRows > 0) {
							return this.res.json({"Error" : false, "Message" : "Success"});
						}

					}).bind(this));

				} else if(rows.length > 0) {

					var query = "UPDATE iodt SET device_id = NULL WHERE device_id = ?";
					var values = [this.req.params.device_id];
					query = mysql.format(query, values);
					mySQLHelper.executeSQLQuery(query, function(err, rows) {});

					var query = "DELETE FROM devices WHERE device_id = ?";
					var values = [this.req.params.device_id];
					query = mysql.format(query, values);

					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "Error in deleteing existing device. Please try again."});
						} else if(rows.affectedRows > 0) {
							return this.res.json({"Error" : false, "Message" : "Success"});
						}

					}).bind(this));
				}

			}).bind(this));
		}

	}).bind(params));

});


module.exports = router;
