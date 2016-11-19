# -*- coding: UTF-8 -*-
"""
The Document class and associated globals
"""

from collections import namedtuple

from spectacle.data_layer.document_data import db_get_document_by_id
from spectacle.data_layer.document_data import db_add_document
from spectacle.data_layer.document_data import db_edit_document
from spectacle.data_layer.document_data import db_publish_document
from spectacle.data_layer.document_data import db_get_all_unpublished_doc_ids
from spectacle.data_layer.document_data import db_get_documents_published_by_user
from spectacle.data_layer.document_data import db_get_documents_submitted_by_user


class Document(namedtuple(
    'Document', [
        'id',
        'title',
        'topic_id',
        'content',
        'summary',
        'original_url',
        'source',
        'date_added',
        'date_published',
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
                        summary=doc.summary,
                        original_url=doc.original_url,
                        source=doc.source,
                        date_added=doc.date_added,
                        date_published=doc.date_published,
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
                        summary=doc.summary,
                        original_url=doc.original_url,
                        source=doc.source,
                        date_added=doc.date_added,
                        date_published=doc.date_published,
                        published=doc.published,
                        )
    return None


def get_all_unpublished_doc_ids():
    return db_get_all_unpublished_doc_ids()


def add_document(title, topic_id, content, summary, original_url, source, user_id=None):
    doc_id = db_add_document(title, topic_id, content, summary, original_url, source, user_id)
    return doc_id


def edit_document(doc_id, title, topic_id, content, summary, original_url, source):
    db_edit_document(doc_id, title, topic_id, content, summary, original_url, source)
    return None


def publish_document(doc_id, user_id):
    db_publish_document(doc_id, user_id)
    return None


def get_submitted_document_ids_by_user(user_id):
    return [
        doc.id
        for doc in db_get_documents_submitted_by_user(user_id)
    ]


def get_published_document_ids_by_user(user_id):
    return [
        doc.id
        for doc in db_get_documents_published_by_user(user_id)
    ]
