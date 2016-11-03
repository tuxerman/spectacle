# -*- coding: UTF-8 -*-
"""
ORM and data functions for Document
"""
from playhouse.sqlite_ext import SqliteExtDatabase
from spectacle.data_layer.document_data import Document, FTSEntry

DATABASE = 'documents.db'

database = SqliteExtDatabase(DATABASE, threadlocals=True)


def create_tables():
    database.connect()
    database.create_tables([Document, FTSEntry])


def before_request_handler():
    database.connect()


def after_request_handler():
    database.close()


create_tables()
