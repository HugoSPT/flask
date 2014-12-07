from ConfigParser import ConfigParser
import cPickle as pickle
import json
import requests
import pika

from backend.feed.util.QueueHandler import \
	RabbitQueueHandler

config = ConfigParser()
config.read('../../../config.cfg')

QUEUE_WORKER = config.get('Queue', 'workers').split(',')
QUEUE_DB = config.get('Queue', 'db')
RABBIT_MQ_IP = config.get('System', 'Rabbit')

class Worker(object):

	def __init__(self, worker_no):
		self.worker_no = worker_no
		self.exchange_queue_handler = RabbitQueueHandler('impakt')
		self.consumer = self.exchange_queue_handler.cons_register(QUEUE_WORKER[self.worker_no])

		self.consumer.consume_task(self.callback)

	def callback(self, body):
		tweet = pickle.loads(body)

		key = 'get_%s' % (QUEUE_WORKER[self.worker_no])
		result = None

		if hasattr(self, key):
			result = getattr(self, key)(tweet)

		if result['action'] == 'sentiment':
			tweet['positive'] = result['positive']
			tweet['negative'] = result['negative']

		connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_MQ_IP))
		channel 	= connection.channel()

		channel.queue_declare(queue=QUEUE_DB)

		channel.basic_publish(exchange='', 
			routing_key=QUEUE_DB, 
			body=pickle.dumps(tweet), 
			properties=pika.BasicProperties(
				delivery_mode = 2, # make message persistent
			)
		)

		connection.close()

	def get_localization(self, tweet):
		pass

	def get_sentiment(self, tweet):
		text = tweet['text']

		r = requests.post("http://text-processing.com/api/sentiment/", data=dict(text=text))

		if r.status_code == 200:
			result = json.loads(r.text)
			tmp = dict()
			tmp['action'] = 'sentiment'
			tmp['positive'] = result['probability']['pos']
			tmp['negative'] = result['probability']['neg']
			
			return tmp

		return None



def run(worker_no):
	worker = Worker(worker_no)

