
var express = require('express');
var logger = require('morgan');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var mysql = require("mysql");

var config = require('./config');
var mySQLHelper = require('./helper/mySQLHelper');

var users = require('./routes/users');
var clusters = require('./routes/clusters');
var devices = require('./routes/devices');
var iodt = require('./routes/iodt');


var app = express();
var port = config.app.port || 7000;

mySQLHelper.createMySQLPool();

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(__dirname + '/public'));

app.use('/api/users', users);
app.use('/api/clusters', clusters);
app.use('/api/devices', devices);
app.use('/api/iodt', iodt);

setInterval(function() {
	updateStatusOfDevices();
}, 360000);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
	var err = new Error('Not Found');
	err.status = 404;
	next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
	app.use(function(err, req, res, next) {
		res.status(err.status || 500);
		res.send({
			message: err.message,
			error: err
		});
		return;
	});
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
	res.status(err.status || 500);
	res.send({
		message: err.message,
		error: err
	});
	return;
});

function updateStatusOfDevices() {
	var query = "UPDATE devices SET status = 'inactive', updated_at= NOW() WHERE NOT DATE_SUB(NOW(), INTERVAL 1 HOUR) < updated_at";
	var values = [];

	query = mysql.format(query, values);

	mySQLHelper.executeSQLQuery(query, function(err, rows) {
		if(err) {
			console.log(err);
		}
	});
}

app.listen(port);
console.log('IoDT Application Running on port: ' + port);

module.exports = app;
