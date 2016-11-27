# -*- coding: UTF-8 -*-
"""
Document views
"""
from flask import jsonify, request
import spectacle.document.logic as document_logic
from application import application
from spectacle.user.utils import get_current_user_info


@application.route('/document/submit', methods=['POST'])
def submit_document():
    user_info = get_current_user_info()
    doc_data = request.form
    new_doc_id = document_logic.add_document(
        title=doc_data['title'],
        topic_id=doc_data['topic_id'],
        content='',  # content
        summary=doc_data['summary'],
        original_url=doc_data['original_url'],
        source=doc_data['source'],
        user_id=user_info.get('username')
    )
    return jsonify({'id': new_doc_id})


@application.route('/document/publish/<int:docid>', methods=['POST'])
def publish_document(docid):
    user_info = get_current_user_info()
    doc_data = request.form
    document_logic.edit_document(
        docid,
        title=doc_data['title'],
        topic_id=doc_data['topic_id'],
        content=doc_data['content'],
        summary=doc_data['summary'],
        original_url=doc_data['original_url'],
        source=doc_data['source']
    )
    document_logic.publish_document(docid, user_id=user_info['username'])
    return jsonify({'success': True})
