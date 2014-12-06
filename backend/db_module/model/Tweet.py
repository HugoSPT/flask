__author__ = 'filipe'
from mongoengine import \
    Document, \
    StringField, \
    DecimalField, \
    DateTimeField

class Tweet(Document):
    id_str = StringField()
    name = StringField()
    text = StringField()
    loc = StringField()
    sentiment = DecimalField()
    created_at = DateTimeField()


