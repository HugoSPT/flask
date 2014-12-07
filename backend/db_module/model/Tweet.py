__author__ = 'filipe'
from mongoengine import \
    Document, \
    StringField, \
    DecimalField, \
    DateTimeField

class Tweet(Document):
    tweetId = StringField()
    user = StringField()
    text = StringField()
    location = StringField()
    negative = DecimalField()
    positive = DecimalField()
    created_at = DateTimeField()


