import ConfigParser
import pika
import cPickle as pickle
import logging


config = ConfigParser.ConfigParser()
config.read('../../config.cfg')

RABBIT_MQ_IP = config.get("System", "rabbit")

class RabbitQueueHandler(object):

	def __init__(self, exchange=None):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_MQ_IP))
		self.channel 	= self.connection.channel()
		self.ex         = exchange
		if self.ex:
			self.channel.exchange_declare(exchange=self.ex, type='direct')

	def pub_register(self, routing_key, queue_bind):
		return RabbitPublisher(routing_key, queue_bind, self)

	def cons_register(self, routing_key):
		return RabbitConsumer(routing_key, self)

	def close_conn(self):
		self.connection.close()


class RabbitPublisher(RabbitQueueHandler):

	def __init__(self, routing_key, queue_bind, parent):
		self.parent 		= parent
		self.channel 		= self.parent.channel
		self.routing_key    = routing_key

		self.channel.queue_bind(exchange='impakt', queue=queue_bind)

	def create_queue(self):
		self.channel.queue_declare(queue=self.routing_key)

	def publish_task(self, data):
		for key in self.routing_key:
			print key
			self.publish(data, key)

	def publish(self, data, key):
		exchange = self.parent.ex if self.parent.ex else ''

		message_promise = self.channel.basic_publish(
			exchange 		= exchange,
			routing_key 	= key,
			body 			= data,
			properties 		= pika.BasicProperties(
                         		delivery_mode = 2, # make message persistent
                      		)
		)

class RabbitConsumer(RabbitQueueHandler):
	def __init__(self, routing_key, parent):
		self.parent 		= parent
		self.channel 		= self.parent.channel
		self.routing_key    = routing_key
		self.result 		= self.channel.queue_declare(queue=self.routing_key)

		for key in self.routing_key:
			if self.parent.ex:
				self.channel.queue_bind(
						exchange     = self.parent.ex,
						queue        = self.routing_key,
						routing_key  = key # binding_key
					)
			else:
				self.channel.queue_declare(
						queue        = self.routing_key
					)

	def consume_task(self, cb):
		self.cb = cb

		self.channel.basic_consume(
			self.callback,
			queue=self.routing_key,
		)

		self.channel.start_consuming()

	def callback(self, ch, method, properties, body):
		ch.basic_ack(delivery_tag=method.delivery_tag)
		self.cb(body)
