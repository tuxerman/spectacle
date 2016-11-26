# -*- coding: UTF-8 -*-
"""
Delete all existing tables and create new ones, initialise new users
"""
import simplejson as json
from elasticsearch import Elasticsearch

from spectacle.database_definitions import CURRENT_DATABASE
from spectacle.document.model import Document, SubmittedDocument, PublishedDocument
from spectacle.user.model import User, db_add_user, db_promote_user
from spectacle.user.utils import hash_pass
from spectacle.database_definitions import ES_INDEX_MAPPING

from config import ES_INDEX, ES_HOST, ES_PORT

PRIMARY_TABLES = [SubmittedDocument, PublishedDocument, Document, User]


def delete_fts_index(es_host, es_port, es_index):
    print 'Deleting FTS index'
    es = Elasticsearch([{'host': es_host, 'port': es_port}])
    es.indices.delete(index=es_index, ignore=[400, 404])


def create_primary_tables(database):
    print 'Creating primary tables'
    database.connect()
    database.create_tables(PRIMARY_TABLES)


def delete_primary_tables():
    print 'Deleting primary tables'
    for table in PRIMARY_TABLES:
        table.drop_table(fail_silently=True)


def create_users():
    """
    {"username": "admin", "password": "password", "email": "abc@xyz.com", "is_moderator": true}
    {"username": "user", "password": "password", "email": "abc@xyz.com", "is_moderator": false}
    """
    print 'Creating users'
    with open('preload_users.txt', 'r') as users_file:
        for line in users_file:
            try:
                user_info = json.loads(line)
                db_add_user(
                    user_info['username'],
                    hash_pass(user_info['password']),
                    user_info['email'],
                )
                if user_info['is_moderator']:
                    db_promote_user(user_info['username'])
            except Exception as e:
                print e
                # ignore json decode errors, db insertion errors (duplicate users, etc.)
                continue


def create_fts_index(es_host, es_port, es_index, es_index_mapping):
    print 'Creating FTS index'
    es = Elasticsearch([{'host': es_host, 'port': es_port}])
    es.indices.create(index=es_index, ignore=400, body=json.dumps(es_index_mapping))


if __name__ == '__main__':
    delete_primary_tables()
    create_primary_tables(CURRENT_DATABASE)
    delete_fts_index(ES_HOST, ES_PORT, ES_INDEX)
    create_fts_index(ES_HOST, ES_PORT, ES_INDEX, ES_INDEX_MAPPING)
    create_users()
    print 'Done.'
