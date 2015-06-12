var express = require('express');
var http = require('http');
var path = require('path');
var logger = require('morgan')
// var bodyParser = require('body-parser')
var methodOverride = require('method-override')
var errorhandler = require('errorhandler')
// var cons = require('consolidate');
var inspect = require('util').inspect;
// var database = require('mariasql');
var pg = require('pg');

var web3 = require("web3")
var cors = require('cors')

// var bcrypt = require('bcrypt-nodejs');
var app = express();
// var conString = "postgres://db:password@localhost/main";
// var db = new pg();
// db.connect({
// 	host: '127.0.0.1',
// 	user: 'db',
// 	password: 'password',
// 	db: 'db'
// });
// db.on(
// 	'connect', function() {console.log('Connected to Postgres');
// 	var modules = {"bcrypt": bcrypt, "database": database, "db": db, "inspect": inspect};
// 	require('./routes')(app, modules);
// 	}
// ).on(
// 	'error', function() {console.log('Error Connecting to Maria');}
// ).on(
// 	'close', function(hadError){console.log('Connection closed');}
// );
// all environments

app.use(cors());

app.set('port', process.env.PORT || 8050);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.engine('.html', require('ejs').renderFile);
// app.engine('.html', require('jade'));
app.use(logger('dev'));
// app.use(bodyParser());
app.use(methodOverride());
// app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(errorhandler());
}

require('./routes')(app);

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
