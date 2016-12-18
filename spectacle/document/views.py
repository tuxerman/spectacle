# -*- coding: UTF-8 -*-
"""
Document views
"""
import json
import urllib2
from flask import jsonify, request

from application import application
from config import RECAPTCHA_SECRET_KEY
from spectacle.database_definitions import CURRENT_DATABASE
import spectacle.document.logic as document_logic
from spectacle.user.utils import get_current_user_info


@application.route('/document/submit', methods=['POST'])
def submit_document():
    user_info = get_current_user_info()
    doc_data = request.form

    # if not logged in, check bad captcha
    if not user_info['logged_in'] and not _verify_recaptcha(doc_data.get('g_recaptcha_response')):
        return jsonify({'id': None})

    # successful POSTs
    return jsonify(_add_document(
        doc_data['title'], doc_data['summary'], doc_data['original_url'], doc_data['source'], user_info.get('username')
    ))


@CURRENT_DATABASE.atomic()
def _add_document(title, summary, original_url, source, user_id):
    new_doc_id = document_logic.add_document(
        title=title,
        topic_id=-1,
        content='',
        summary=summary,
        original_url=original_url,
        source=source,
        user_id=user_id,
    )
    return {'id': new_doc_id}


@application.route('/document/publish/<int:docid>', methods=['POST'])
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


def _verify_recaptcha(g_recaptcha_response):
    if not g_recaptcha_response:
        return False

    url = "https://www.google.com/recaptcha/api/siteverify?secret={}&response={}".format(
        RECAPTCHA_SECRET_KEY, g_recaptcha_response
    )

    g_result = json.loads(urllib2.urlopen(url).read())
    return g_result['success']
