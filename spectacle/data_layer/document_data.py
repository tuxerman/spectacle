# -*- coding: UTF-8 -*-
"""
ORM and data functions for Document
"""
from peewee import CharField, DateTimeField, TextField, IntegerField, BooleanField
from datetime import datetime

from spectacle.data_layer.database_definitions import CURRENT_BASE_MODEL
from spectacle.data_layer.full_text_search import db_index_document


class Document(CURRENT_BASE_MODEL):
    title = CharField()
    topic_id = IntegerField()
    content = TextField()
    summary = TextField()
    original_url = CharField()
    source = CharField()
    date_added = DateTimeField()
    date_published = DateTimeField()
    published = BooleanField()

    class Meta:
        order_by = ('id',)


def db_get_document_by_id(doc_id):
    return Document.get(Document.id == doc_id)


def db_get_all_unpublished_doc_ids():
    return [
        doc.id
        for doc in Document.select() \
            .where(Document.published == False) \
            .order_by(Document.date_added.desc()
        )
    ]


def db_publish_document(doc_id):
    doc = Document.get(Document.id == doc_id)
    already_published = doc.published
    doc.published = True
    doc.date_published = datetime.now()
    doc.save()
    if not already_published:
        db_index_document(doc)


def db_add_document(title, topic_id, content, summary, original_url, source):
    new_document = Document.create(
        title=title,
        topic_id=topic_id,
        content=content,
        summary=summary,
        original_url=original_url,
        source=source,
        date_added=datetime.now(),
        date_published=datetime(2000, 01, 01, 00, 00, 00),
        published=False,
    )
    return new_document.id


def db_edit_document(doc_id, title, topic_id, content, summary, original_url, source):
    doc = Document.get(Document.id == doc_id)
    if not doc:
        return None
    doc.title = title
    doc.topic_id = topic_id
    doc.content = content
    doc.summary = summary
    doc.original_url = original_url
    doc.source = source
    doc.save()
