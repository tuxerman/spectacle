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


class Document(BaseModel):
    title = CharField()
    topic_id = IntegerField()
    content = TextField()
    original_url = CharField()
    source = CharField()
    date_added = DateTimeField()
    date_published = DateTimeField()
    published = BooleanField()

    class Meta:
        order_by = ('id',)


class FTSEntry(FTSModel):
    entry_id = IntegerField()
    content = TextField()

    class Meta:
        database = database


def db_get_document_by_id(doc_id):
    return Document.get(Document.id == doc_id)


def db_get_document_by_title(title):
    return Document.get(Document.title == title)


def db_publish_document(doc_id):
    doc = Document.get(Document.id == doc_id)
    already_published = doc.published
    doc.published = True
    doc.date_published = datetime.now()
    doc.save()
    if not already_published:
        FTSEntry.create(
            entry_id=doc.id,
            content='\n'.join((doc.title, doc.content)))


def db_add_document(title, topic_id, content, original_url, source):
    new_document = Document.create(
        title=title,
        topic_id=topic_id,
        content=content,
        original_url=original_url,
        source=source,
        date_added=datetime.now(),
        date_published=datetime(2000, 01, 01, 00, 00, 00),
        published=False,
    )
    return new_document.id


def db_edit_document(doc_id, title, topic_id, content, original_url, source):
    doc = Document.get(Document.id == doc_id)
    if not doc:
        return None
    doc.title = title
    doc.topic_id = topic_id
    doc.content = content
    doc.original_url = original_url
    doc.source = source
    doc.save()
