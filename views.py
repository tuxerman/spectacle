from flask import jsonify, render_template, request
import spectacle.flightdeck.document as document_logic
from spectacle.flightdeck.search import search_documents
from app import app
from flask import abort
from flask.ext.stormpath import groups_required, login_required, user


def _user_info_dict(current_user):
    user_info = {'logged_in': False, 'user_id': None, 'is_moderator': False}
    if current_user.is_authenticated:
        user_info['username'] = current_user.username
        user_info['logged_in'] = True
        user_info['is_moderator'] = (
            'moderators' in (group.name for group in current_user.groups)
        )
    return user_info


@app.route('/', methods=['GET'])
def www_show_home():
    return render_template(
        'homepage.html',
        user_info=_user_info_dict(user)
    )


@app.route('/submit', methods=['GET'])
def www_show_submit():
    return render_template('submit_document.html')


@app.route('/review', methods=['GET'])
@groups_required(['moderators'])
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
        user_info=_user_info_dict(user)
    )


@app.route('/dashboard', methods=['GET'])
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

    user_info = _user_info_dict(user)
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


@app.route('/document/<int:docid>', methods=['GET'])
def www_view_document(docid):
    doc_data = document_logic.get_published_document(docid)
    if doc_data:
        return render_template(
            'view_document.html',
            document_data=doc_data)
    else:
        abort(404)


@app.route('/document/review/<int:docid>', methods=['GET'])
@login_required
@groups_required(['moderators'])
def www_review_document(docid):
    doc_data = document_logic.get_document(docid)
    if doc_data:
        return render_template(
            'review_document.html',
            document_data=doc_data)
    else:
        abort(404)


@app.route('/pdf_document/<string:filename>', methods=['GET'])
def get_pdf(filename):
    # https://gist.github.com/jessejlt/1306827 for tips on downloadable PDFs
    return app.send_static_file('pdf/' + filename)


@app.route('/document/search', methods=['GET'])
def search():
    search_string = request.args.get('query')
    return jsonify(search_documents(search_string))


@app.route('/document/submit', methods=['POST'])
def submit_document():
    user_info = _user_info_dict(user)
    doc_data = request.form
    new_doc_id = document_logic.add_document(
        title=doc_data['title'],
        topic_id=doc_data['topic_id'],
        content='',  # content
        summary=doc_data['summary'],
        original_url=doc_data['original_url'],
        source=doc_data['source'],
        user_id=user_info['username']
    )
    return jsonify({'id': new_doc_id})


@app.route('/document/publish/<int:docid>', methods=['POST'])
@groups_required(['moderators'])
def publish_document(docid):
    user_info = _user_info_dict(user)
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


@app.route('/popular', methods=['GET'])
def popular():
    return jsonify([
        {'title': 'List of somethings for 2016', 'id': 2},
        {'title': 'List of something elses for 2015', 'id': 5},
        {'title': 'Goings on for XYZ', 'id': 9},
        {'title': 'Proceedings of the Society for P.T.O.T.O.T', 'id': 13},
        {'title': 'Whos Who of What', 'id': 10},
    ])
