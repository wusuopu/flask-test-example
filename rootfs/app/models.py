#!/usr/bin/env python
# encoding: utf-8

import os
from flask_security import (MongoEngineUserDatastore, UserMixin, RoleMixin)
from flask_mongoengine import MongoEngine
import flask_mongoengine.connection
import mongoengine
import bson
import datetime
import pytz

__CONFIGURED = False
db = MongoEngine()


DateTimeField = db.DateTimeField
StringField = db.StringField
ListField = db.ListField
DictField = db.DictField
IntField = db.IntField
FloatField = db.FloatField
DecimalField = db.DecimalField
URLField = db.URLField
ReferenceField = db.ReferenceField
BooleanField = db.BooleanField
ObjectIdField = db.ObjectIdField
BinaryField = db.BinaryField



def utc_now():
    return datetime.datetime.now(pytz.UTC)


def update_modified(sender, document, *args, **kwargs):
    document.updated_at = utc_now()


class BaseDocument(db.DynamicDocument):
    created_at = mongoengine.fields.DateTimeField(default=utc_now)
    updated_at = mongoengine.fields.DateTimeField(default=utc_now)
    meta = {'abstract': True, 'index_background': True}

# 在数据更新时同时更新 updated_at 字段的值
mongoengine.signals.pre_save.connect(update_modified)


class User(BaseDocument, UserMixin):
    """
    用户信息
    """
    last_login_at = DateTimeField()
    current_login_at = DateTimeField()
    last_login_ip = StringField()
    current_login_ip = StringField()
    login_count = IntField()
    email = StringField(max_length=255)
    password = StringField(max_length=255, default='')
    active = BooleanField(default=True)
    roles = ListField(ReferenceField('Role'), default=[])

    def __str__(self):
        return str(self.id)

    def to_json(self):
        data = {}
        for key in self._fields:
            f = self._fields[key]
            value = v = getattr(self, key)
            if isinstance(f, DateTimeField) and v:
                value = v.timestamp() * 1000
            if isinstance(f, ListField):
                value = []
                for o in v:
                    value.append(str(o))
            data[key] = value
        return data

    meta = {
        'collection': 'users',
    }


class Role(BaseDocument, RoleMixin):
    """
    用户角色
    """
    name = StringField(max_length=80, unique=True)
    meta = {'collection': 'roles'}

    def __str__(self):
        return self.name

UserDatastore = MongoEngineUserDatastore(None, User, Role)


def config(app=None):
    if os.environ.get('FLASK_ENV') == 'test':
        # 测试环境下，使用mongomock
        DB_NAME = 'test_logosmart'
        HOST = "mongomock://localhost:27017/%s" % (DB_NAME)
        mongoengine.connect(DB_NAME, host=HOST, alias='default')
    else:
        USER_HOST = os.environ.get(
            'MONGO_URI',
            'mongodb://mongodb:27017/authentication?ssl=false&ssl_cert_reqs=CERT_NONE'
        )
        MONGODB_SETTINGS = [
            {'alias': 'default', 'host': USER_HOST},
        ]
        if app:
            app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS
            db.init_app(app)
        else:
            flask_mongoengine.connection.create_connections(
                {'MONGODB_SETTINGS': MONGODB_SETTINGS}
            )
