# import Tweet do Cabaco

class Tweet(object):
	def __init__(self, tweet_id):
		self.tweet_id = tweet_id
		self.in_db = False

	def load(self):
		rs = Tweet.objects(tweetId=self.tweetId)

		if rs:
			self.in_db = True

			

	def parse_json(self)