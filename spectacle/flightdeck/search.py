# -*- coding: UTF-8 -*-
"""
The Search module
"""
from spectacle.data_layer.document_data import Document
from spectacle.data_layer.full_text_search import db_search_documents


def search_documents(query_string):
    results = db_search_documents(query_string)
    return results
