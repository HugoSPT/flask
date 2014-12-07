'use strict';

//Server Web Socket

var app  = require('express')();
var http = require('http').Server(app);
var io   = require('socket.io')(http);
var cos  = require('./consumer')
var gm   = cos.getMsg;

function WebSocket() {
}

var socket = WebSocket.prototype;
module.exports.WebSocket = socket;

socket.socket_array = [];

socket.useArray = function (msg) {
	for(var i = 0; i < this.socket_array.length; i++) {
		console.log("Socket: " + i + " msg: " + msg);
		this.socket_array[i].emit('msg', msg);
	}
}

socket.init = function(req, res) {
	io.on('connection', function(sock) {
		socket.socket_array[socket.socket_array.length] = sock;
	});

	http.listen(3001, function() {
		console.log("Listening")
	});

	app.get('/', function(req, res) {
		res.sendFile('/home/ivo/git/flask/backend/provider/frontend/test.html');
	});
}