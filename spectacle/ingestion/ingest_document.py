# -*- coding: UTF-8 -*-
"""
Batch to read a JSON file containing all information about a document, and ingest the document into the system
"""

from __future__ import print_function
from collections import namedtuple
import simplejson as json
import sys

from spectacle.document import add_document


class DocumentData(namedtuple(
    'DocumentData', [
        'title',
        'topic_id',
        'content',
        'original_url',
        'local_filepath',
        'source',
        'metadata',
    ]
)):
    pass


def save_locally(filepath):
    pass


def main():
    try:
        filepath = sys.argv[1]
    except IndexError:
        sys.exit(1)

    with open(filepath, 'r') as f:
        doc_data = DocumentData(json.load(f))
        doc_id = add_document(title=doc_data.title,
                              topic_id=doc_data.topic_id,
                              content=doc_data.content,
                              original_url=doc_data.original_url,
                              source=doc_data, source)

        # make a local copy with the doc_id as the name
        save_locally(doc_data.local_filepath)

        print('Added document id: {}'.format(doc_id))


if __name__ == '__main__':
    main()
