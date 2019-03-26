# -*- coding: utf-8 -*-
import os

from peewee import BooleanField, Model, SqliteDatabase, TextField, UUIDField

from playhouse.sqlite_ext import JSONField

_path = os.path.expanduser('~/.asyncy/services.db')
_db = SqliteDatabase(_path)


class DB:

    def __init__(self):
        pass

    class BaseModel(Model):
        class Meta:
            database = _db

    class Service(BaseModel):
        service_uuid = UUIDField(primary_key=True)
        name = TextField(index=True)
        alias = TextField(index=True, null=True)
        username = TextField()
        description = TextField(null=True)
        certified = BooleanField()
        public = BooleanField()
        topics = JSONField(null=True)
        state = TextField()
        configuration = JSONField()
        readme = TextField(null=True)

    def __enter__(self):
        _db.connect(reuse_if_open=True)
        _db.create_tables([DB.Service])
        return _db

    def __exit__(self, exc_type, exc_val, exc_tb):
        _db.close()
