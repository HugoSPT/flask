__author__ = 'filipe'
import ConfigParser
import mongoengine
from model.Tweet import Tweet

def createTweet(tweetId,user,loc,sentiment):
    tweet = Tweet()
    tweet.tweetId = tweetId
    tweet.user = user
    tweet.loc = loc
    tweet.sentiment = sentiment
    tweet.save()

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('../../config.cfg')

mongoengine.connect('TweetInTime',host=config.get('System', 'mongo'))
rs = Tweet.objects()
newTweet = Tweet
createTweet("test","test","loc",0)
for result in rs :
    print(result.user)

