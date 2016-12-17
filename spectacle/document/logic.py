# -*- coding: UTF-8 -*-
"""
The Document class and associated globals
"""
from collections import namedtuple

from spectacle.document.model import db_get_document_by_id
from spectacle.document.model import db_add_document
from spectacle.document.model import db_edit_document
from spectacle.document.model import db_publish_document
from spectacle.document.model import db_get_all_docs_fetched
from spectacle.document.model import db_get_all_docs_submitted
from spectacle.document.model import db_get_documents_published_by_user
from spectacle.document.model import db_get_documents_submitted_by_user
from spectacle.document.model import db_set_state
from spectacle.document.model import DocState


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
        'state'
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
                        state=doc.state,
                        )
    return None


def get_published_document(doc_id):
    doc = db_get_document_by_id(doc_id)
    if doc and doc.state == DocState.published:
        return Document(id=doc.id,
                        title=doc.title,
                        topic_id=doc.topic_id,
                        content=doc.content,
                        summary=doc.summary,
                        original_url=doc.original_url,
                        source=doc.source,
                        date_added=doc.date_added,
                        date_published=doc.date_published,
                        state=doc.state,
                        )
    return None


def get_all_doc_ids_fetched():
    return [doc.id for doc in db_get_all_docs_fetched()]


def get_all_doc_ids_submitted():
    return [doc.id for doc in db_get_all_docs_submitted()]


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


def mark_doc_as_fetched(doc_id):
    db_set_state(doc_id, DocState.fetched)


def mark_doc_as_discarded(doc_id):
    db_set_state(doc_id, DocState.discarded)
