# -*- coding: UTF-8 -*-
"""
Create table
"""
import simplejson as json
from elasticsearch import Elasticsearch

from spectacle.data_layer.database_setup import CURRENT_DATABASE
from spectacle.data_layer.document_data import Document, SubmittedDocument, PublishedDocument
from spectacle.data_layer.user import User, db_add_user, hash_pass, db_promote_user
from spectacle.data_layer.database_setup import ES_INDEX_MAPPING

from config import ES_INDEX, ES_HOST, ES_PORT

PRIMARY_TABLES = [SubmittedDocument, PublishedDocument, Document, User]


def delete_fts_index(es_host, es_port, es_index):
    es = Elasticsearch([{'host': es_host, 'port': es_port}])
    es.indices.delete(index=es_index, ignore=[400, 404])


def create_primary_tables(database):
    database.connect()
    database.create_tables(PRIMARY_TABLES)


def delete_primary_tables():
    for table in PRIMARY_TABLES:
        table.drop_table(fail_silently=True)


def create_users():
    db_add_user('admin', hash_pass('password'))
    db_add_user('pleb', hash_pass('password'))
    db_promote_user('admin')


def create_fts_index(es_host, es_port, es_index, es_index_mapping):
    es = Elasticsearch([{'host': es_host, 'port': es_port}])
    es.indices.create(index=es_index, ignore=400, body=json.dumps(es_index_mapping))


delete_primary_tables()
create_primary_tables(CURRENT_DATABASE)
create_users()
delete_fts_index(ES_HOST, ES_PORT, ES_INDEX)
create_fts_index(ES_HOST, ES_PORT, ES_INDEX, ES_INDEX_MAPPING)
