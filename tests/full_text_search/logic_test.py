# -*- coding: UTF-8 -*-
"""
Logic functions for ElasticSearch FTS Index
"""
from spectacle.full_text_search.model import db_search_documents


def search_documents(query_string, page_size, start_page):
    results = db_search_documents(query_string, page_size, start_page)
    return results
