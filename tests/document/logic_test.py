# -*- coding: UTF-8 -*-
import mock

from spectacle.document.model import DocState
import spectacle.document.logic as document_logic
import spectacle.document.model as document_model


@mock.patch('spectacle.document.logic.db_get_document_by_id')
def test_get_document(mock_db_get_document_by_id):
    mock_doc_model = mock.Mock(spec=document_model.Document)
    mock_db_get_document_by_id.return_value = mock_doc_model
    doc = document_logic.get_document(42)
    assert doc == document_logic.Document(
        id=mock_doc_model.id,
        title=mock_doc_model.title,
        topic_id=mock_doc_model.topic_id,
        content=mock_doc_model.content,
        summary=mock_doc_model.summary,
        original_url=mock_doc_model.original_url,
        source=mock_doc_model.source,
        date_added=mock_doc_model.date_added,
        date_published=mock_doc_model.date_published,
        state=mock_doc_model.state,
    )


@mock.patch('spectacle.document.logic.db_get_document_by_id')
def test_get_non_existent_document(mock_db_get_document_by_id):
    mock_db_get_document_by_id.return_value = None
    doc = document_logic.get_document(42)
    assert doc is None


def test_get_published_document(mock_db_get_document_by_id):
    mock_doc_model = mock.Mock(spec=document_model.Document, state=document_model.DocState.published)
    mock_db_get_document_by_id.return_value = mock_doc_model
    doc = document_logic.get_document(42)
    assert doc == document_logic.Document(
        id=mock_doc_model.id,
        title=mock_doc_model.title,
        topic_id=mock_doc_model.topic_id,
        content=mock_doc_model.content,
        summary=mock_doc_model.summary,
        original_url=mock_doc_model.original_url,
        source=mock_doc_model.source,
        date_added=mock_doc_model.date_added,
        date_published=mock_doc_model.date_published,
        state=mock_doc_model.state,
    )


def test_get_published_document_returns_none_for_not_published(mock_db_get_document_by_id):
    for doc_state in [DocState.submitted, DocState.fetched, DocState.discarded]:
        mock_doc_model = mock.Mock(spec=document_model.Document, state=doc_state)
        mock_db_get_document_by_id.return_value = mock_doc_model
        doc = document_logic.get_document(42)
        assert doc is None


'''
def get_all_doc_ids_fetched():
    return [doc.id for doc in db_get_all_docs_fetched()]


def get_all_doc_ids_submitted():
    return [doc.id for doc in db_get_all_docs_submitted()]


def add_document(title, topic_id, content, summary, original_url, source, user_id=None):
    doc_id = db_add_document(title, topic_id, content, summary, original_url, source, user_id)
    return doc_id


def edit_document(doc_id, title, topic_id, content, summary, original_url, source):
    db_edit_document(doc_id, title, topic_id, content, summary, original_url, source)
    return None


def publish_document(doc_id, user_id):
    db_publish_document(doc_id, user_id)
    return None


def get_submitted_document_ids_by_user(user_id):
    return [
        doc.id
        for doc in db_get_documents_submitted_by_user(user_id)
    ]


def get_published_document_ids_by_user(user_id):
    return [
        doc.id
        for doc in db_get_documents_published_by_user(user_id)
    ]


def mark_doc_as_fetched(doc_id):
    db_set_state(doc_id, DocState.fetched)


def mark_doc_as_discarded(doc_id):
    db_set_state(doc_id, DocState.discarded)
'''
