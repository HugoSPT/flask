__author__ = 'filipe'
import ConfigParser
import mongoengine
import datetime
import cPickle as pickle
from model.Tweet import Tweet
from backend.feed.util.QueueHandler import \
	RabbitQueueHandler


config = ConfigParser.ConfigParser()
config.read('../../config.cfg')

class DbModule():
    def __init__(self):
        mongoengine.connect(config.get('System', 'mongo-db-name'),host=config.get('System', 'mongo'))
    def create_tweet(self,tweetJson):
        tweet = self.get_tweet(tweetJson.id_str)
        if not tweet:
            tweet = Tweet()
        for attr in tweet._fields.keys():
            if not attr == 'id':
                setattr(tweet, attr, tweetJson[attr])
        tweet.save()

    def get_tweet(self,id_str):
        tweet =  Tweet.objects(id_str=id_str)
        return tweet[0] if tweet else None

class Rabbitmq():
    dbModule = DbModule()
    def __init__(self):
        self.queue_handler = RabbitQueueHandler()
        self.consumer = self.queue_handler.cons_register(config.get('Queue', 'db'))
        self.run()
    def run(self):
        while True:
            tweet = self.consumer.consume_task()
            if tweet:
                dbModule.create_tweet(tweet)
                print pickle.loads(tweet)


if __name__ == '__main__':config = \
dbModule = Rabbitmq()