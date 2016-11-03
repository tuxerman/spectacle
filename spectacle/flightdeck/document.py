# -*- coding: UTF-8 -*-
"""
The Document class and associated globals
"""

from collections import namedtuple

from spectacle.data_layer.document_data import db_get_document_by_id
from spectacle.data_layer.document_data import db_add_document


class Document(namedtuple(
    'Document', [
        'id',
        'title',
        'topic_id',
        'content',
        'original_url',
        'source',
        'date_added',
    ]
)):
    pass


def get_document(doc_id):
    doc = db_get_document_by_id(doc_id)
    if doc:
        return Document(id=doc.id, title=doc.title, topic_id=doc.topic_id, content=doc.content, original_url=doc.original_url, source=doc.source, date_added=doc.date_added)
    return None


def add_document(title, topic_id, content, original_url, source):
    doc_id = db_add_document(title, topic_id, content, original_url, source)
    return doc_id
