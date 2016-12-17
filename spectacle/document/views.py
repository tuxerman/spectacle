# -*- coding: UTF-8 -*-
"""
Document views
"""
from flask import jsonify, request
from flask_login import login_required
import spectacle.document.logic as document_logic
from application import application
from spectacle.user.utils import get_current_user_info
from spectacle.database_definitions import CURRENT_DATABASE
from spectacle.user.utils import moderators_only


@application.route('/document/submit', methods=['POST'])
@CURRENT_DATABASE.atomic()
def submit_document():
    user_info = get_current_user_info()
    doc_data = request.form
    new_doc_id = document_logic.add_document(
        title=doc_data['title'],
        topic_id=-1,
        content='',  # content
        summary=doc_data['summary'],
        original_url=doc_data['original_url'],
        source=doc_data['source'],
        user_id=user_info.get('username')
    )
    return jsonify({'id': new_doc_id})


@application.route('/document/publish/<int:docid>', methods=['POST'])
@login_required
@moderators_only
@CURRENT_DATABASE.atomic()
def publish_document(docid):
    user_info = get_current_user_info()
    doc_data = request.form
    document_logic.edit_document(
        docid,
        title=doc_data['title'],
        topic_id=-1,
        content=doc_data['content'],
        summary=doc_data['summary'],
        original_url=doc_data['original_url'],
        source=doc_data['source']
    )
    document_logic.publish_document(docid, user_id=user_info['username'])
    return jsonify({'success': True})


@application.route('/document/discard/<int:docid>', methods=['POST'])
@login_required
@moderators_only
@CURRENT_DATABASE.atomic()
def discard_submitted_document(docid):
    document_logic.mark_doc_as_discarded(docid)
    return jsonify({'success': True})
