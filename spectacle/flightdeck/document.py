# -*- coding: UTF-8 -*-
"""
The Document class and associated globals
"""

from collections import namedtuple

from spectacle.data_layer.document import db_get_document_from_id
from spectacle.data_layer.document import db_add_document
from spectacle.data_layer.document import db_add_metadata


class Document(namedtuple(
    'Document', [
        'doc_id',
        'title',
        'topic_id',
        'content',
        'original_url',
        'source',
        'date_added',
        'metadata',
    ]
)):
    pass


class DocumentMetaData(namedtuple(
    'DocumentMetaData', [
        'version',
        'doc_id',
        'genre',
        'link_is_live',
    ]
)):
    pass


def document_from_id(doc_id):
    return db_get_document_from_id(doc_id)


def add_document(title, topic_id, content, original_url, source):
    doc_id = db_add_document()
    return doc_id


def add_metadata_to_document(doc_id, metadata_json):
    metadata_id = db_add_metadata(doc_id, metadata_json)
    return metadata_id


def url_for_local_copy(doc_id):
    return './docstorage/{}'.format(doc_id)
