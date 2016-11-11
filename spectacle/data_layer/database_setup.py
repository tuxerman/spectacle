# -*- coding: UTF-8 -*-
"""
ORM and data functions for Document
"""
from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import MySQLDatabase
from peewee import Model


SQLITE_DB = SqliteExtDatabase('documents.db', threadlocals=True)
MYSQL_DB = MySQLDatabase(
    "documents", host="127.0.0.1", port=3306, user="sriram", passwd="password")

CURRENT_DATABASE = SQLITE_DB


class SqliteModel(Model):
    class Meta:
        database = SQLITE_DB


class MySQLModel(Model):
    class Meta:
        database = MYSQL_DB


def before_request_handler(database):
    database.connect()


def after_request_handler(database):
    database.close()


CURRENT_BASE_MODEL = SqliteModel
