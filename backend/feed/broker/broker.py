from ConfigParser import ConfigParser

from backend.feed.util.QueueHandler import \
	RabbitQueueHandler

config = ConfigParser()
config.read('../../../config.cfg')

QUEUE_FEED = config.get('Queue', 'feed')
QUEUES_WORKERS = config.get('Queue', 'workers')

class Broker(object):
	def __init__(self):
		self.queue_handler = RabbitQueueHandler()
		self.consumer = self.queue_handler.cons_register(QUEUE_FEED)
		self.publisher = self.queue_handler.pub_register(QUEUES_WORKERS)

		self.run()

	def run(self):
		while True:

			task = self.consumer.consume_task()

			if task:
				self.publisher.publish_task(task)


def run():
	broker = Broker()

if __name__ == '__main__':
	run()