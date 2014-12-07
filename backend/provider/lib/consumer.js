'use strict';

var amqp      = require('amqplib');
var FEED_NAME = "X";
var ssocket = require('./serversocket')
var socket  = ssocket.WebSocket;

var msgs = []

function init() {
	var connection = amqp.connect('amqp://192.168.1.73');
	connection.then(function(conn) {
	    return conn.createChannel().then(function(ch) {

	        var queue = ch.assertQueue(FEED_NAME, {durable: false});

	        queue = queue.then(function() {
	            return ch.consume(FEED_NAME, function(msg) {
	                ch.ack(msg);
	               	msgs[msgs.length] = msg.content.toString();
	               	socket.useArray(msgs[msgs.length-1]);
	            });
	        });

	        return queue.then(function() {
	        	console.log(' [*] Waiting for messages. To exit press CTRL+C');
	        });
	    });
	}).then(null, console.warn);
}

module.exports.init = init;
