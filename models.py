import datetime
from flask import url_for
from __init__ import db

class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=255, required=True)
    age = db.IntField(required=True)

    def get_absolute_url(self):
        return url_for('user', kwargs={"name": self.name})

    def __unicode__(self):
        return self.name

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'name'],
        'ordering': ['-created_at']
    }