exports = module.exports = function(app){
	// var backend = require("./routes/mariaaccounts.js");
	// backend.init(libs);

	app.use(function(req, res, next) {
	  res.header("Access-Control-Allow-Origin", "*");
	  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	  next();
	});
	//HomePage
	app.get('/', require('./views/index').init);

	app.get('/join/', require('./views/join/join').init);
	app.get('/send/', require('./views/send/send').init);
	app.get('/thanks/', require('./views/thanks/thanks').init);
}
