# -*- coding: UTF-8 -*-
"""
ORM and data functions for Document
"""
import simplejson as json
from elasticsearch import Elasticsearch

from spectacle.data_layer.database_setup import ES_INDEX_MAPPING


HOST = 'localhost'
PORT = 9200
INDEX = 'testindex_02'

# Define a default Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index=INDEX, ignore=400, body=json.dumps(ES_INDEX_MAPPING))


def db_index_document(document):
    es.index(index=INDEX,
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


def _fuzzy_search_query(query_string):
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
        }
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


def db_search_documents(query_string):
    response = es.search(index=INDEX, body=_fuzzy_search_query(query_string))
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
