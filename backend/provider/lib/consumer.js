var amqp      = require('amqplib');
var FEED_NAME = "FEED";

function init() {
	var connection = amqp.connect('amqp://192.168.1.73');
	
	connection.then(function(conn) {
	    return conn.createChannel().then(function(ch) {

	        var queue = ch.assertQueue(FEED_NAME, {durable: false});

	        queue = queue.then(function() {
	            return ch.consume(FEED_NAME, function(msg) {
	                console.log(msg.content.toString());
	                ch.ack(msg);
	                return;
	            });
	        });

	        return queue.then(function() {
	        	console.log(' [*] Waiting for messages. To exit press CTRL+C');
	        });
	    });
	}).then(null, console.warn);
}

module.exports = init;