__author__ = 'filipe'
from mongoengine import \
    Document, \
    StringField, \
    DecimalField


class Tweet(Document):
    tweetId = StringField()
    user = StringField()
    loc = StringField()
    sentiment = DecimalField()


