# -*- coding: UTF-8 -*-
"""
Script to extract text from PDF and add it to the contents
"""
import os
import urllib

from spectacle.flightdeck.document import edit_document
from spectacle.flightdeck.document import get_all_unpublished_doc_ids
from spectacle.flightdeck.document import get_document


DOWNLOAD_DIR = "static/pdf/"


def download_file(url, filename):
    full_file_path = os.path.join(DOWNLOAD_DIR, filename)
    urllib.urlretrieve(url, full_file_path)
    return full_file_path


def extract_text_from_doc(filename):
    try:
        import textract
        return textract.process(filename).replace('\n', ' ')
    except ImportError:
        return 'Could not extract content from document'


def main():
    for doc_id in get_all_unpublished_doc_ids():
        doc = get_document(doc_id)
        if doc.content:
            print 'Skipping id: {}, title: ({})'.format(doc.id, doc.title)
            continue

        print 'Processing id: {}, title: {}'.format(doc.id, doc.title)
        downloaded_file_path = download_file(doc.original_url, '{}.pdf'.format(doc_id))
        edit_document(
            doc_id=doc.id,
            title=doc.title,
            topic_id=doc.topic_id,
            content=extract_text_from_doc(downloaded_file_path),
            summary=doc.summary,
            original_url=doc.original_url,
            source=doc.source
        )


if __name__ == '__main__':
    main()
