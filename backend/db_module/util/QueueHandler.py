import pika
import cPickle as pickle
import logging


class RabbitQueueHandler(object):

	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.65'))
		self.channel 	= self.connection.channel()
		self.channel.exchange_declare(exchange='impakt', type='direct')

	def pub_register(self, routing_key):
		return RabbitPublisher(routing_key, self)

	def cons_register(self, routing_key):
		return RabbitConsumer(routing_key, self)

	def close_conn(self):
		self.connection.close()


class RabbitPublisher(RabbitQueueHandler):

	def __init__(self, routing_key, parent):
		self.parent 		= parent
		self.channel 		= self.parent.channel
		self.routing_key    = routing_key
		self.i = 0

	def publish_task(self, data, keys=None):
		if not keys:
			for key in self.routing_key:
				self.publish(data, key)
		else:
			for key in keys:
				if key in self.routing_key:
					self.publish(data, key)
				else:
					logging.error("The key %s is not valid for the register.", key)

	def publish(self,data, key):
		message_promise = self.channel.basic_publish(
			exchange 		= 'impakt',
			routing_key 	= key,
			body 			= data,
			properties 		= pika.BasicProperties(
                         		delivery_mode = 2, # make message persistent
                      		)
		)
		#self.i += 1
		#print "SELF I:", self.i


class RabbitConsumer(RabbitQueueHandler):
	def __init__(self, routing_key, parent):
		self.parent 		= parent
		self.channel 		= self.parent.channel
		self.routing_key    = routing_key
		self.result 		= self.channel.queue_declare(exclusive=True)
		self.queue_name 	= self.result.method.queue
		self.i = 0

		for key in self.routing_key:
			self.channel.queue_bind(
						exchange     = 'impakt',
						queue        = self.queue_name,
						routing_key  = key # binding_key
					)

	def consume_task(self):
		method_frame, header_frame, body = self.channel.basic_get(
						queue  = self.queue_name,
						no_ack = False,
					)
		if body:
			#print ' Message received'
			#print
			#print ' Waiting for messages. To exit press CTRL+C'
			#self.i += 1
			#print "RECEIVED I: ", self.i
			return body