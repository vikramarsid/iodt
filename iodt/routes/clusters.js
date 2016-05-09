
var express = require('express');
var router = express.Router();
var mysql = require("mysql");

var mySQLHelper = require('../helper/mySQLHelper');
var web3Helper = require('../helper/web3Helper');
var stringUtils = require('../helper/stringUtils');


/* GET all clusters listing */
router.get('/', function(req, res) {

	var query = "SELECT * FROM clusters";
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No clusters present."});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Clusters" : rows});
		}

	}).bind(params));

});


/* GET cluster by cluster_id */
/* PARAMS cluster_id */
router.get('/:cluster_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.cluster_id)) {
		return res.json({"Error" : false, "Message" : "No cluster_id specified"});
	}

	var query = "SELECT * FROM clusters WHERE cluster_id = ?";
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
			return this.res.json({"Error" : false, "Message" : "Cluster with cluster ID '" + this.req.params.cluster_id + "' is not present"});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Clusters" : rows});
		}

	}).bind(params));

});


/* GET all clusters for user_name */
/* PARAMS user_name */
router.get('/user/:user_name', function(req, res) {

	if(stringUtils.isEmpty(req.params.user_name)) {
		return res.json({"Error" : false, "Message" : "No user_name specified"});
	}

	var query = "SELECT cluster_id FROM iodt WHERE user_name = ?";
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
			return this.res.json({"Error" : false, "Message" : "No clusters present for user name '" + this.req.params.user_name + "'"});
		} else if(rows.length > 0) {

			var cluster_id_array = [];
			for(var row in rows) {
				cluster_id_array.push(rows[row].cluster_id);
			}
			var query = "SELECT * FROM clusters WHERE cluster_id IN (?)";
			var values = [cluster_id_array];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {
					return this.res.json({"Error" : false, "Message" : "No clusters present for user name '" + this.req.params.user_name + "'"});
				} else if(rows.length > 0) {
					return this.res.json({"Error" : false, "Message" : "Success", "Clusters" : rows});
				}

			}).bind(this));
		}

	}).bind(params));

});


/* POST create cluster */
/* PARAMS user_name */
/* BODY name, description, power_limit */
router.post('/user/:user_name', function(req, res) {

	if(stringUtils.isEmpty(req.params.user_name) || stringUtils.isEmpty(req.body.name) || stringUtils.isEmpty(req.body.description) || stringUtils.isEmpty(req.body.power_limit)) {
		return res.json({"Error" : true, "Message" : "No name and/or description given to a cluster"});
	}

	var query = "SELECT * FROM devices WHERE device_id IN (?)";
	var values = [req.body.device_id];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		try {
			var web3Obj = web3Helper.createWeb3(rows[0].host, rows[0].rpcport);
			for (var i = 1; i < rows.length; i++) {
				var peerAddress = "enode://" + rows[i].enode + "@" + rows[i].host + ":" + rows[i].port;
				web3Obj.admin.addPeer(peerAddress);
			};
		} catch(err) {
			return res.json({"Error" : false, "Message" : "Error while creating new cluster. Please try again."});
		}

		var query = "INSERT INTO clusters (name, description, power_limit, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW())";
		var values = [this.req.body.name, this.req.body.description, this.req.body.power_limit];
		query = mysql.format(query, values);
		mySQLHelper.executeSQLQuery(query, (function(err, rows) {

			if(err) {
				return this.res.json({"Error" : true, "Message" : err});
			} else if(rows.affectedRows == 0) {
				return this.res.json({"Error" : false, "Message" : "Error while creating new cluster. Please try again."});
			} else if(rows.affectedRows > 0) {

				var query = "SELECT * FROM clusters ORDER BY cluster_id DESC LIMIT 1";
				var values = [];
				query = mysql.format(query, values);
				mySQLHelper.executeSQLQuery(query, (function(err, rows) {

					if(err) {
						return this.res.json({"Error" : true, "Message" : err});
					} else if(rows.length == 0) {
						return this.res.json({"Error" : false, "Message" : "No cluster found for user '" + this.req.params.user_name + "'"});
					} else if(rows.length > 0) {

						if(typeof this.req.body.device_id != "object") {
							this.req.body.device_id = [this.req.body.device_id];
						}
						for(var i = 0; i < this.req.body.device_id.length; i++) {
							var query = "INSERT INTO iodt (user_name, cluster_id, device_id, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW())";
							var values = [this.req.params.user_name, rows[0].cluster_id, this.req.body.device_id[i]];
							query = mysql.format(query, values);
							mySQLHelper.executeSQLQuery(query, function(err, rows) {});
						}

						return this.res.json({"Error" : false, "Message" : "Success", "Clusters" : rows});
					}

				}).bind(this));
			}

		}).bind(this));

	}).bind(params));

});


/* PUT update cluster */
/* PARAMS cluster_id */
/* BODY name, description, power_limit */
router.put('/:cluster_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.cluster_id) || stringUtils.isEmpty(req.body.name) || stringUtils.isEmpty(req.body.description) || stringUtils.isEmpty(req.body.power_limit)) {
		return res.json({"Error" : true, "Message" : "No name and/or description given to a cluster"});
	}

	var query = "SELECT * FROM clusters WHERE cluster_id = ?";
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
			return this.res.json({"Error" : false, "Message" : "Cluster with cluster id '" + this.req.params.cluster_id + "' is not present"});
		} else if(rows.length > 0) {

			var query = "UPDATE clusters SET name = ?, description = ?, power_limit = ?, updated_at = NOW() WHERE cluster_id = ?";
			var values = [this.req.body.name, this.req.body.description, this.req.body.power_limit, this.req.params.cluster_id];
			query = mysql.format(query, values);
			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.affectedRows == 0) {
					return this.res.json({"Error" : false, "Message" : "Error while updating existing cluster. Please try again."});
				} else if(rows.affectedRows > 0) {

					var query = "SELECT * FROM clusters WHERE cluster_id = ?";
					var values = [this.req.params.cluster_id];
					query = mysql.format(query, values);
					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "No cluster found with id '" + this.req.params.cluster_id + "'"});
						} else if(rows.length > 0) {
							return this.res.json({"Error" : false, "Message" : "Success", "Clusters" : rows});
						}

					}).bind(this));
				}

			}).bind(this));
		}

	}).bind(params));

});


/* DELETE cluster by cluster_id */
/* PARAMS cluster_id */
router.delete('/:cluster_id', function(req, res) {

	if(stringUtils.isEmpty(req.params.cluster_id)) {
		return res.json({"Error" : false, "Message" : "No cluster_id specified"});
	}

	var query = "SELECT * FROM clusters WHERE cluster_id = ?";
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
			return this.res.json({"Error" : false, "Message" : "Cluster with cluster id '" + this.req.params.cluster_id + "' is not present"});
		} else if(rows.length > 0) {

			var query = "SELECT device_id FROM iodt WHERE cluster_id = ?";
			var values = [this.req.params.cluster_id];
			query = mysql.format(query, values);

			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {

					var query = "DELETE FROM clusters WHERE cluster_id = ?";
					var values = [this.req.params.cluster_id];
					query = mysql.format(query, values);

					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "Error in deleteing existing cluster. Please try again."});
						} else if(rows.affectedRows > 0) {
							return this.res.json({"Error" : false, "Message" : "Success"});
						}

					}).bind(this));

				} else if(rows.length > 0) {

					for(var row in rows) {
						if(rows[row].device_id == null) {
						} else {
							return this.res.json({"Error" : false, "Message" : "Cannot delete a cluster which has devices. Please try again."});
						}
					}
					var query = "DELETE FROM iodt WHERE cluster_id = ?";
					var values = [this.req.params.cluster_id];
					query = mysql.format(query, values);

					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "Error in deleteing existing cluster. Please try again."});
						} else if(rows.affectedRows > 0) {

							var query = "DELETE FROM clusters WHERE cluster_id = ?";
							var values = [this.req.params.cluster_id];
							query = mysql.format(query, values);

							mySQLHelper.executeSQLQuery(query, (function(err, rows) {

								if(err) {
									return this.res.json({"Error" : true, "Message" : err});
								} else if(rows.length == 0) {
									return this.res.json({"Error" : false, "Message" : "Error in deleteing existing cluster. Please try again."});
								} else if(rows.affectedRows > 0) {
									return this.res.json({"Error" : false, "Message" : "Success"});
								}

							}).bind(this));
						}

					}).bind(this));
				}

			}).bind(this));
		}

	}).bind(params));

});


module.exports = router;
