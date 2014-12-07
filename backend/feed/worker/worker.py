from ConfigParser import ConfigParser
import cPickle as pickle
import requests

from backend.feed.util.QueueHandler import \
	RabbitQueueHandler

config = ConfigParser()
config.read('../../../config.cfg')

QUEUE_WORKER = config.get('Queue', 'workers').split(',')
QUEUE_DB = config.get('Queue', 'db')

class Worker(object):

	def __init__(self, worker_no):
		self.worker_no = worker_no
		self.exchange_queue_handler = RabbitQueueHandler('impakt')
		self.consumer = self.exchange_queue_handler.cons_register(QUEUE_WORKER[self.worker_no])

		self.simple_queue_handler = RabbitQueueHandler('')
		self.publisher = self.simple_queue_handler.pub_register(QUEUE_DB)
		self.publisher.create_queue()

		self.consumer.consume_task(self.callback)

	def callback(self, body):
		tweet = pickle.loads(body)

		key = 'get_%s' % (QUEUE_WORKER[self.worker_no])
		result = None

		if hasattr(self, key):
			result = getattr(self, key)(tweet)

		if result:
			tweet[result['action']] = result[result['action']]

		self.publisher.publish_task(body)

	def get_localization(self, tweet):
		pass

	def get_sentiment(self, tweet):
		text = tweet['text']

		r = requests.post("http://text-processing.com/api/sentiment/", data=dict(text=text))

		if r.status_code == 200:
			result = r.text
			result['action'] = 'sentiment'
			result['sentiment']['label'] = result['label']
			result['sentiment']['probability']['positive'] = result['probability']['pos']
			result['sentiment']['probability']['negative'] = result['probability']['neg']
			
			return result

		return None



def run(worker_no):
	worker = Worker(worker_no)

