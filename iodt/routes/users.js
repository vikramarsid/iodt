
var express = require('express');
var router = express.Router();
var mysql = require("mysql");

var mySQLHelper = require('../helper/mySQLHelper');
var stringUtils = require('../helper/stringUtils');


/* GET all users listing */
router.get('/', function(req, res) {

	var query = "SELECT * FROM users";
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "No users present."});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Users" : rows});
		}

	}).bind(params));

});


/* GET user by user_name */
/* PARAMS user_name */
router.get('/:user_name', function(req, res) {

	if(stringUtils.isEmpty(req.params.user_name)) {
		return res.json({"Error" : false, "Message" : "No user_name specified"});
	}

	var query = "SELECT * FROM users WHERE user_name = ?";
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
			return this.res.json({"Error" : false, "Message" : "User with user name '" + this.req.params.user_name + "' is not present"});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Users" : rows});
		}

	}).bind(params));

});


/* POST user login */
/* BODY user_name, password */
router.post('/login', function(req, res) {

	if(stringUtils.isEmpty(req.body.user_name) || stringUtils.isEmpty(req.body.password)) {
		return res.json({"Error" : true, "Message" : "No user_name and/or password specified"});
	}

	var query = "SELECT * FROM users WHERE user_name = ? && password = ?";
	var values = [req.body.user_name, req.body.password];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "Incorrect user name and/or password"});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "Success", "Users" : rows});
		}

	}).bind(params));

});


/* POST method to register a new user */
/* BODY user_name, name, email, password, number, gender, dob, address */
router.post('/register', function(req, res) {

	if(stringUtils.isEmpty(req.body.user_name) || stringUtils.isEmpty(req.body.name) || stringUtils.isEmpty(req.body.email) || stringUtils.isEmpty(req.body.password) || stringUtils.isEmpty(req.body.number) || stringUtils.isEmpty(req.body.gender) || stringUtils.isEmpty(req.body.dob) || stringUtils.isEmpty(req.body.address)) {
		return res.json({"Error" : true, "Message" : "All values are mandatory"});
	}

	var query = "SELECT * FROM users WHERE user_name = ? OR email = ?";
	var values = [req.body.user_name, req.body.email];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res,
	}
	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length > 0) {
			return this.res.json({"Error" : false, "Message" : "User ID and/or E-Mail already in use"});
		}

		var query = "INSERT INTO users (user_name, name, email, password, number, gender, dob, address, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW())";
		var values = [this.req.body.user_name, this.req.body.name, this.req.body.email, this.req.body.password, this.req.body.number, this.req.body.gender, this.req.body.dob, this.req.body.address];
		query = mysql.format(query, values);
		mySQLHelper.executeSQLQuery(query, (function(err, rows) {

			if(err) {
				return this.res.json({"Error" : true, "Message" : err});
			} else if(rows.affectedRows == 0) {
				return this.res.json({"Error" : false, "Message" : "Error while registering new user. Please try again."});
			} else if(rows.affectedRows > 0) {

				var query = "SELECT * FROM users WHERE user_name = ?";
				var values = [this.req.body.user_name];
				query = mysql.format(query, values);
				mySQLHelper.executeSQLQuery(query, (function(err, rows) {

					if(err) {
						return this.res.json({"Error" : true, "Message" : err});
					} else if(rows.length == 0) {
						return this.res.json({"Error" : false, "Message" : "User with user name '" + this.req.params.user_name + "' is not present"});
					} else if(rows.length > 0) {
						return this.res.json({"Error" : false, "Message" : "Success", "Users" : rows});
					}

				}).bind(this));
			}

		}).bind(this));

	}).bind(params));

});


/* PUT method to update an existing user */
/* PARAMS user_name */
/* BODY name, email, password, number, gender, dob, address */
router.put('/update/:user_name', function(req, res) {

	if(stringUtils.isEmpty(req.body.user_name) || stringUtils.isEmpty(req.body.name) || stringUtils.isEmpty(req.body.email) || stringUtils.isEmpty(req.body.password) || stringUtils.isEmpty(req.body.number) || stringUtils.isEmpty(req.body.gender) || stringUtils.isEmpty(req.body.dob) || stringUtils.isEmpty(req.body.address)) {
		return res.json({"Error" : true, "Message" : "All values are mandatory"});
	}

	var query = "SELECT * FROM users WHERE user_name = ? AND email = ?";
	var values = [req.params.user_name, req.body.email];
	query = mysql.format(query, values);
	var params = {
		'req': req,
		'res': res,
	}

	mySQLHelper.executeSQLQuery(query, (function(err, rows) {

		if(err) {
			return this.res.json({"Error" : true, "Message" : err});
		} else if(rows.length == 0) {
			return this.res.json({"Error" : false, "Message" : "User ID and/or E-Mail not found"});
		} else if(rows.length > 0) {

			var query = "UPDATE users SET name = ?, password = ?, number = ?, gender = ?, dob = ?, address = ?, updated_at = NOW() WHERE user_name = ? AND email = ?";
			var values = [this.req.body.name, this.req.body.password, this.req.body.number, this.req.body.gender, this.req.body.dob, this.req.body.address, this.req.params.user_name, this.req.body.email];
			query = mysql.format(query, values);

			mySQLHelper.executeSQLQuery(query, (function(err, rows) {

				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.affectedRows == 0) {
					return this.res.json({"Error" : false, "Message" : "Error in updating existing user. Please try again."});
				} else if(rows.affectedRows > 0) {

					var query = "SELECT * FROM users WHERE user_name = ?";
					var values = [this.req.params.user_name];
					query = mysql.format(query, values);
					mySQLHelper.executeSQLQuery(query, (function(err, rows) {

						if(err) {
							return this.res.json({"Error" : true, "Message" : err});
						} else if(rows.length == 0) {
							return this.res.json({"Error" : false, "Message" : "User with user name '" + this.req.params.user_name + "' is not present"});
						} else if(rows.length > 0) {
							return this.res.json({"Error" : false, "Message" : "Success", "Users" : rows});
						}

					}).bind(this));
				}

			}).bind(this));
		}

	}).bind(params));

});


/* DELETE user by user_name */
/* PARAMS user_name */
router.delete('/:user_name', function(req, res) {

	if(stringUtils.isEmpty(req.params.user_name)) {
		return res.json({"Error" : false, "Message" : "No user_name specified"});
	}

	var query = "SELECT * FROM users WHERE user_name = ?";
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
			return this.res.json({"Error" : false, "Message" : "User with user name '" + this.req.params.user_name + "' is not present"});
		} else if(rows.length > 0) {

			var query = "DELETE FROM users WHERE user_name = ?";
			var values = [this.req.params.user_name];
			query = mysql.format(query, values);

			mySQLHelper.executeSQLQuery(query, (function(err, rows) {
				if(err) {
					return this.res.json({"Error" : true, "Message" : err});
				} else if(rows.length == 0) {
					return this.res.json({"Error" : false, "Message" : "Error in deleteing existing user. Please try again."});
				} else if(rows.affectedRows > 0) {
					return this.res.json({"Error" : false, "Message" : "Success"});
				}
			}).bind(this));

		}
	}).bind(params));

});


module.exports = router;
