
var mysql = require("mysql");
var config = require('../config');

var mySQLHelper = {};

mySQLHelper.createMySQLPool = function() {

	mySQLHelper.mySqlPool = mysql.createPool({
		connectionLimit : 100,
		host     : config.mysql.host,
		port     : config.mysql.port,
		user     : config.mysql.user,
		password : config.mysql.password,
		database : config.mysql.database,
		debug    : config.mysql.debug,
	});

};


mySQLHelper.executeSQLQuery = function(query, callback) {

	mySQLHelper.mySqlPool.getConnection(function(err, connection){
		if(err) {
			mySQLHelper.onSQLConnectionError(err);
		} else {
			connection.query(query, function(err, rows) {
				connection.release();
				callback(err, rows);
			});
		}
	});

}


mySQLHelper.onSQLConnectionError = function(err) {
	console.log("Issue with MySQL: " + err);
	// TODO - need to find more on this
	// process.exit(1);
}


module.exports = mySQLHelper;
