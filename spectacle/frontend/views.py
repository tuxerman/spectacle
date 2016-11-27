# -*- coding: UTF-8 -*-
"""
WWW views
"""
from application import application
from flask import render_template
from flask import abort
from flask import Response
from flask_login import login_required
import config
from boto.s3.connection import S3Connection
import boto

import spectacle.document.logic as document_logic
from spectacle.user.utils import moderators_only, get_current_user_info


@application.route('/', methods=['GET'])
def www_show_home():
    return render_template(
        'homepage.html',
        user_info=get_current_user_info()
    )


@application.route('/about', methods=['GET'])
def www_show_about():
    return render_template(
        'about.html',
        user_info=get_current_user_info()
    )


@application.route('/register', methods=['GET'])
def www_show_register():
    return render_template(
        'register.html',
        user_info=get_current_user_info()
    )


@application.route('/submit', methods=['GET'])
def www_show_submit():
    return render_template(
        'submit_document.html',
        user_info=get_current_user_info())


@application.route('/review', methods=['GET'])
@login_required
@moderators_only
def www_show_review_dashboard():

    def doc_review_data(doc):
        return {
            'id': doc.id,
            'title': doc.title,
            'date_added': doc.date_added.strftime("%d %b %Y, %H:%M"),
            'source': doc.source
        }

    docs_to_review = [
        doc_review_data(document_logic.get_document(doc_id))
        for doc_id in document_logic.get_all_unpublished_doc_ids()
    ]
    return render_template(
        'review_dashboard.html',
        docs_to_review=docs_to_review,
        user_info=get_current_user_info()
    )


@application.route('/dashboard', methods=['GET'])
@login_required
def www_show_user_dashboard():
    def doc_submission_data(doc):
        return {
            'id': doc.id,
            'title': doc.title,
            'date_added': doc.date_added.strftime("%d %b %Y, %H:%M"),
            'date_published': (
                doc.date_published.strftime("%d %b %Y, %H:%M")
                if doc.published else 'Pending'
            ),
            'source': doc.source
        }

    user_info = get_current_user_info()
    user_id = user_info['username']
    docs_submitted, docs_published = [], []
    # TODO: Why are we calling get_doc() on IDs which were filtered in the first place?
    docs_submitted = [
        doc_submission_data(document_logic.get_document(doc_id))
        for doc_id in
        document_logic.get_submitted_document_ids_by_user(user_id)
    ]
    if user_info['is_moderator']:
        docs_published = [
            doc_submission_data(document_logic.get_document(doc_id))
            for doc_id in
            document_logic.get_published_document_ids_by_user(user_id)
        ]
    return render_template(
        'user_dashboard.html',
        docs_submitted=docs_submitted,
        docs_published=docs_published,
        user_info=user_info,
    )


@application.route('/document/<int:docid>', methods=['GET'])
def www_view_document(docid):
    def doc_view_data(doc):
        return {
            'id': doc.id,
            'title': doc.title,
            'topic_id': doc.topic_id,
            'summary': doc.summary,
            'original_url': doc.original_url,
            'date_added': doc.date_added.strftime("%d %b %Y, %H:%M"),
            'date_published': doc.date_published.strftime("%d %b %Y, %H:%M"),
            'url': 'https://s3.amazonaws.com/{}/{}.pdf'.format(config.S3_PDF_BUCKET, doc.id),
            'source': doc.source
        }

    document = document_logic.get_published_document(docid)
    if document:
        return render_template(
            'view_document.html',
            document_data=doc_view_data(document),
            user_info=get_current_user_info())
    else:
        abort(404)


@application.route('/document/review/<int:docid>', methods=['GET'])
@login_required
@moderators_only
def www_review_document(docid):
    doc_data = document_logic.get_document(docid)
    if doc_data:
        return render_template(
            'review_document.html',
            document_data=doc_data,
            user_info=get_current_user_info())
    else:
        abort(404)


@application.route('/pdf_document/<string:filename>', methods=['GET'])
def get_pdf_from_s3(filename):
    # https://gist.github.com/jessejlt/1306827 for tips on downloadable PDFs
    # return application.send_static_file('pdf/' + filename)

    # stream test
    conn = S3Connection(config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
    bucket = conn.get_bucket(config.S3_PDF_BUCKET, validate=False)
    key = bucket.get_key(filename)
    try:
        key.open_read()
        headers = dict(key.resp.getheaders())
        return Response(key, headers=headers)
    except boto.exception.S3ResponseError as e:
        return Response(e.body, status=e.status, headers=key.resp.getheaders())
