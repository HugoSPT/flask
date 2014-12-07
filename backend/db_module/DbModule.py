__author__ = 'filipe'
import ConfigParser
import mongoengine
import cPickle as pickle
import pika
from datetime import datetime
from model.Tweet import Tweet
from backend.feed.util.QueueHandler import \
	RabbitQueueHandler


config = ConfigParser.ConfigParser()
config.read('../../config.cfg')

class DbModule():
    def __init__(self):
        mongoengine.connect(config.get('System', 'mongo-db-name'),host=config.get('System', 'mongo'))
    def create_tweet(self,tweetJson):
        try:
            tweet = self.get_tweet(tweetJson["id"])
            if not tweet:
                tweet = Tweet()
            for attr in tweet._fields.keys():
                if not attr == 'id':
                    if tweetJson.has_key(attr):
                        if attr == "user":
                            setattr(tweet, attr, tweetJson["user"]["screen_name"])
                        elif attr == "created_at":
                            setattr(tweet, attr, datetime.strptime(tweetJson["created_at"],"%a %b %d %H:%M:%S +0000 %Y"))
                        else:
                            setattr(tweet, attr, tweetJson[attr])
                    else:
                        setattr(tweet, "tweetId", str(tweetJson["id"]))
            tweet.save()
            connection = pika.BlockingConnection(pika.ConnectionParameters(config.get('System', 'Rabbit')))
            channel 	= connection.channel()
            channel.queue_declare(queue=config.get('Queue', 'client'))
            channel.basic_publish(exchange='',
                                  routing_key=config.get('Queue', 'client'),
                                  body=tweet.to_json(),
                                  properties=pika.BasicProperties(
                                      delivery_mode = 2,
                                      )
            )
        except Exception , e:
            raise

    def get_tweet(self,tweetId):
        tweet =  Tweet.objects(tweetId=tweetId)
        return tweet[0] if tweet else None

class Rabbitmq():
    def __init__(self):
        self.queue_handler = RabbitQueueHandler("")
        self.consumer = self.queue_handler.cons_register(config.get('Queue', 'db'))
        self.dbModule = DbModule()
        self.run()
    def cb(self,body):
        tweet = pickle.loads(body)
        self.dbModule.create_tweet(tweet)
    def run(self):
        tweet = self.consumer.consume_task(self.cb)



if __name__ == '__main__':config = \
Rabbitmq()

