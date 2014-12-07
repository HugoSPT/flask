var express = require('express');
var router  = express.Router();
var ssocket = require('../lib/serversocket')
var socket  = ssocket.WebSocket;

/* GET home page. */
router.get('/', function(req, res) {
  	socket.init(req, res);
  	res.send('<h1>Hello world</h1>');
});

module.exports = router;
