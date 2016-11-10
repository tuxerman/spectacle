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
    return '''
        The Supreme Court has extensive original jurisdiction
        for the protection of fundamental rights of citizens. It also acts
        as the court to settle disputes between various governments in the country.
        As an advisory court, it hears matters which may specifically be referred
        to it under the Constitution by the President. It also may take cognisance
        of matters on its own (or 'suo moto'), without anyone drawing its attention.
    '''


def main():
    for doc_id in get_all_unpublished_doc_ids():
        doc = get_document(doc_id)
        if doc.content:
            print 'Skipping {} ({})'.format(doc.id, doc.title)
            continue

        downloaded_file_path = download_file(doc.original_url, "{}.pdf".format(doc_id))
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
