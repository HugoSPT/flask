from ConfigParser import ConfigParser
import cPickle as pickle
import pika

from backend.feed.util.QueueHandler import \
	RabbitQueueHandler

config = ConfigParser()
config.read('../../../config.cfg')

QUEUE_FEED = config.get('Queue', 'feed')
QUEUES_WORKERS = config.get('Queue', 'workers').split(',')

class Broker(object):
	def __init__(self):
		self.simple_queue_handler = RabbitQueueHandler()
		self.consumer = self.simple_queue_handler.cons_register(QUEUE_FEED)

		self.exchange_queue_handler = RabbitQueueHandler('impakt')
		self.publisher = self.exchange_queue_handler.pub_register(QUEUES_WORKERS, 'sentiment')

		self.consumer.consume_task(self.callback)


	def callback(self, body):
		self.task = pickle.loads(body)

		print self.task['id']

		self.publisher.publish_task(pickle.dumps(self.task))

		self.task = None

def run():
	broker = Broker()

if __name__ == '__main__':
	run()