from ConfigParser import ConfigParser
import cPickle as pickle

from backend.feed.util.QueueHandler import \
	RabbitQueueHandler

config = ConfigParser()
config.read('../../../config.cfg')

QUEUE_WORKER = config.get('Queue', 'workers').split(',')

class Worker(object):

	def __init__(self, worker_no):
		self.worker_no = worker_no
		self.queue_handler = RabbitQueueHandler()
		self.consumer = self.queue_handler.cons_register(QUEUE_WORKER[self.worker_no])

		self.consume()

	def consume(self):
		while True:

			task = self.consumer.consume_task()

			if task:
				tweet = pickle.loads(task)

				print tweet

				key = 'get_%s' % (QUEUE_WORKER[self.worker_no])

				if hasattr(self, key):
					getattr(self, key)(tweet)

	def get_localization(self, tweet):
		pass

	def get_sentiment(self, tweet):
		text = tweet['text']

def run(worker_no):
	worker = Worker(worker_no)

