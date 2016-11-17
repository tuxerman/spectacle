# -*- coding: UTF-8 -*-
"""
ORM and data functions for Document
"""
from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import MySQLDatabase
from peewee import Model

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB
from config import SQLITE_FILEPATH
from config import CURRENT_DATABASE_TYPE


SQLITE_DB = SqliteExtDatabase(SQLITE_FILEPATH, threadlocals=True)
MYSQL_DB = MySQLDatabase(
    MYSQL_DB,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWD,
    charset='utf8mb4'
)

CURRENT_DATABASE = MYSQL_DB if CURRENT_DATABASE_TYPE == 'mysql' else SQLITE_DB


class SqliteModel(Model):
    class Meta:
        database = SQLITE_DB


class MySQLModel(Model):
    class Meta:
        database = MYSQL_DB


CURRENT_BASE_MODEL = MySQLModel if CURRENT_DATABASE_TYPE == 'mysql' else SqliteModel

ES_INDEX_MAPPING = {
    "mappings": {
        "document": {
            "_all": {"enabled": False},
            "properties": {
                "doc_id": {"type": "integer"},
                "title": {
                    "type": "text",
                    "analyzer": "english"
                },
                "content": {
                    "type": "text",
                    "analyzer": "english"
                },
                "summary": {
                    "type": "text",
                    "analyzer": "english",
                },
            }
        }
    }
}