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

	app.get('/join/', require('./views/join/index').init);
	app.get('/send/', require('./views/send/index').init);
	app.get('/thanks/', require('./views/thanks/index').init);
	//Sign In

	//Sign Up
	// app.get('/signup/', require('./views/signup/index').init);
	// app.post('/signup/', require('./views/signup/index').signup(accountBackend));

	//Sign Out
	//Temporary, Going to be taken out.
	// app.post('/api/createaccount', accountbackend.createAccount);
	// app.post('/api/changeusername', accountbackend.changeUsername);
	// app.post('/api/changeemail', accountbackend.changeEmail);
	// app.post('/api/changepassword', accountbackend.changePassword);
	// app.post('/api/verifyaccount', accountbackend.verifyAccount);
	// app.post('/api/removeaccount', accountbackend.removeAccount);
}
