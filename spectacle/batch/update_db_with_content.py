# -*- coding: UTF-8 -*-
"""
Script to extract text from PDF and add it to the contents
"""
from boto.s3.connection import S3Connection
import os
import urllib

import config
from spectacle.document.logic import edit_document
from spectacle.document.logic import get_all_unpublished_doc_ids
from spectacle.document.logic import get_document


DOWNLOAD_DIR = "static/pdf/"


def _get_s3_connection():
    if not (config.S3_ACCESS_KEY and config.S3_SECRET_KEY):
        return
    return S3Connection(config.S3_ACCESS_KEY, config.S3_SECRET_KEY)


def download_file(url, filename):
    full_file_path = os.path.join(DOWNLOAD_DIR, filename)
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    urllib.urlretrieve(url, full_file_path)
    return full_file_path


def upload_to_s3(connection, filename, filepath):
    bucket = connection.get_bucket(config.S3_PDF_BUCKET)
    key = bucket.new_key(filename)
    with open(filepath, 'r') as f:
        key.set_contents_from_string(
            f.read(),
            headers={
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'inline',
            }
        )
        key.set_canned_acl('public-read')


def extract_text_from_doc(filename):
    try:
        import textract
        return textract.process(filename).replace('\n', ' ')
    except Exception:
        return 'Could not extract content from document'


def main():
    for doc_id in get_all_unpublished_doc_ids():
        doc = get_document(doc_id)
        if doc.content:
            print 'Skipping id: {}, title: ({})'.format(doc.id, doc.title)
            continue

        print 'Processing id: {}, title: {}'.format(doc.id, doc.title)
        downloaded_file_path = download_file(doc.original_url, '{}.pdf'.format(doc_id))
        upload_to_s3(_get_s3_connection(), '{}.pdf'.format(doc_id), downloaded_file_path)
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
