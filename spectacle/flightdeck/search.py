"""
The Search module
"""
from spectacle.data_layer.document_data import FTSEntry, Document


def search_documents(query_string):
    query = (FTSEntry
             .select(Document)
             .join(
                 Document,
                 on=(FTSEntry.entry_id == Document.id).alias('document'))
             .where(FTSEntry.match(query_string))
             .dicts())
    return [{'document': row,
             'snippet': _snippet_from_document(row, query_string)
             }
            for row in query]


def _snippet_from_document(document, query_string):
    return (
        next((sentence
              for sentence in document['content'].split('. ')
              if query_string in sentence
              ), None) or
        document['content'].split('. ')[:2]
    )
