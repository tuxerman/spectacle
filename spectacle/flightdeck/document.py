# -*- coding: UTF-8 -*-
"""
The Document class and associated globals
"""

from collections import namedtuple

from spectacle.data_layer.document_data import db_get_document_by_id
from spectacle.data_layer.document_data import db_add_document
from spectacle.data_layer.document_data import db_edit_document
from spectacle.data_layer.document_data import db_publish_document


class Document(namedtuple(
    'Document', [
        'id',
        'title',
        'topic_id',
        'content',
        'original_url',
        'source',
        'date_added',
        'published'
    ]
)):
    pass


def get_document(doc_id):
    doc = db_get_document_by_id(doc_id)
    if doc:
        return Document(id=doc.id,
                        title=doc.title,
                        topic_id=doc.topic_id,
                        content=doc.content,
                        original_url=doc.original_url,
                        source=doc.source,
                        date_added=doc.date_added,
                        published=doc.published,
                        )
    return None


def get_published_document(doc_id):
    doc = db_get_document_by_id(doc_id)
    if doc and doc.published:
        return Document(id=doc.id,
                        title=doc.title,
                        topic_id=doc.topic_id,
                        content=doc.content,
                        original_url=doc.original_url,
                        source=doc.source,
                        date_added=doc.date_added,
                        published=doc.published,
                        )
    return None


def add_document(title, topic_id, content, original_url, source):
    doc_id = db_add_document(title, topic_id, content, original_url, source)
    return doc_id


def edit_document(doc_id, title, topic_id, content, original_url, source):
    db_edit_document(doc_id, title, topic_id, content, original_url, source)
    return None


def publish_document(doc_id):
    db_publish_document(doc_id)
    return None
