__author__ = 'filipe'
import ConfigParser
import mongoengine
import datetime
from model.Tweet import Tweet


class DbModule():
    def start(self):
        mongoengine.connect('TweetInTime',host=config.get('System', 'mongo'))
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

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('../../config.cfg')
dbModule = DbModule()
dbModule.start()
print dbModule.get_tweet("test")
dbModule.create_tweet(Tweet(id_str="test", name="test",text="aojfdajfalskjdlasjdlksjd",loc="",sentiment=0,created_at=datetime.datetime.now()))
print dbModule.get_tweet("test")