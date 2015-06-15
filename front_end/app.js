var express = require('express');
var http = require('http');
var path = require('path');
var errorhandler = require('errorhandler')

//var cors = require('cors')

// var bcrypt = require('bcrypt-nodejs');
var app = express();

//app.use(cors());

app.set('port', process.env.PORT || 38050);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.engine('.html', require('ejs').renderFile);

app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(errorhandler());
}

require('./routes')(app);

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
