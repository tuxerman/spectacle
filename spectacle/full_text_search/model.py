# -*- coding: UTF-8 -*-
"""
ORM and data functions for ElasticSearch FTS Index
"""
import simplejson as json
from elasticsearch import Elasticsearch

from config import ES_HOST, ES_PORT, ES_INDEX
from spectacle.database_definitions import ES_INDEX_MAPPING


# Define a default Elasticsearch client
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
es.indices.create(index=ES_INDEX, ignore=400, body=json.dumps(ES_INDEX_MAPPING))


def db_index_document(document):
    es.index(
        index=ES_INDEX,
        doc_type='document',
        id=document.id,
        body=_es_doc_from_document(document)
    )


def _es_doc_from_document(document):
    return {
        'doc_id': document.id,
        'title': document.title,
        'content': document.content,
        'summary': document.summary,
    }


def _fuzzy_search_query(query_string, page_size, start_page):
    return {
        "query": {
            "multi_match": {
                "query": query_string,
                "fuzziness": "AUTO",
                "fields": ["title", "summary", "content"],
                "type": "best_fields",
            }
        },
        "highlight": {
            "pre_tags": ["<strong>"],
            "post_tags": ["</strong>"],
            "fields": {
                "summary": {"fragment_size": 140, "number_of_fragments": 1},
                "content": {"fragment_size": 140, "number_of_fragments": 1},
            }
        },
        "size": page_size,
        "from": start_page,
    }


def _get_highlight_from_result(result):
    if not result.get('highlight'):
        return None
    try:
        return result['highlight']['summary']
    except KeyError:
        try:
            return result['highlight']['content']
        except KeyError:
            return None


def db_search_documents(query_string, page_size, start_page):
    page_size = page_size or 5
    start_page = start_page or 0
    response = es.search(
        index=ES_INDEX,
        body=_fuzzy_search_query(query_string, page_size, start_page),
    )
    num_results = response['hits']['total']
    results = response['hits']['hits']
    search_results = {
        'hits': num_results,
        'results': [
            {
                'doc_id': result['_id'],
                'title': result['_source']['title'],
                'snippet': (
                    _get_highlight_from_result(result) or
                    result['_source']['summary'][:140]
                )
            } for result in results
        ]
    }
    return search_results
