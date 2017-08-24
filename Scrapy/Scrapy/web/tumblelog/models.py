import datetime
from flask import url_for
from tumblelog import db
from wtforms import validators
import uuid
from mongoengine.queryset import QuerySet


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)

class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class BlogPost(Post):
    body = db.StringField(required=True)


class Video(Post):
    embed_code = db.StringField(required=True)


class Image(Post):
    image_url = db.StringField(required=True, max_length=255)


class Quote(Post):
    body = db.StringField(required=True)
    author = db.StringField(verbose_name="Author Name", required=True, max_length=255)

class Login(db.DynamicDocument):
    username = db.StringField(max_length=255,verbose_name="username", required=True)
    email = db.StringField(max_length=255,verbose_name="email", required=True)
    password = db.StringField(max_length=255,verbose_name="password", required=True
        ,validators=[validators.InputRequired(message=u'pass not valid'),validators.EqualTo('confirm',message = 'Passwords must match')])
    confirm = db.StringField(max_length=255,verbose_name="Repeat Password",required=True)
    identity = db.StringField(max_length=255,required=True,default=str(uuid.uuid1()))


class Aacargo(db.DynamicDocument):
    airWaybillNumber = db.StringField(max_length=255,verbose_name="AirWaybillNumber",required=True)

class CaptureQueue(db.DynamicDocument):
    captureNo = db.StringField()
    captureStatus = db.StringField()
