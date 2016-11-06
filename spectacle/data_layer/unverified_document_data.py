# -*- coding: UTF-8 -*-
"""
ORM and data functions for Document
"""
from peewee import Model, CharField, DateTimeField, TextField, IntegerField
from playhouse.sqlite_ext import *
from datetime import datetime

DATABASE = 'documents.db'
database = SqliteExtDatabase(DATABASE, threadlocals=True)


class BaseModel(Model):
    class Meta:
        database = database


class UnverifiedDocument(BaseModel):
    title = CharField()
    topic_id = IntegerField()
    content = TextField()
    original_url = CharField()
    source = CharField()
    date_added = DateTimeField()

    class Meta:
        order_by = ('id',)


def db_get_document_by_id(doc_id):
    return Document.get(Document.id == doc_id)


def db_get_document_by_title(title):
    return Document.get(Document.title == title)


def db_add_document(title, topic_id, content, original_url, source):
    new_document = Document.create(
        title=title,
        topic_id=topic_id,
        content=content,
        original_url=original_url,
        source=source,
        date_added=datetime.now()
    )
