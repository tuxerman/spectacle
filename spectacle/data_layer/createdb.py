# -*- coding: UTF-8 -*-
"""
Create table
"""

from spectacle.data_layer.database_setup import CURRENT_DATABASE
from spectacle.data_layer.document_data import Document


def create_tables(database):
    database.connect()
    database.create_tables([Document])


create_tables(CURRENT_DATABASE)
