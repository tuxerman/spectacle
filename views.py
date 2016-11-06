from flask import jsonify, render_template, request
import spectacle.flightdeck.document as document_logic
import spectacle.flightdeck.document as unverified_document_logic
from spectacle.flightdeck.search import search_documents
from app import app


@app.route('/', methods=['GET'])
def show_home():
    return render_template('homepage.html')


@app.route('/home2', methods=['GET'])
def show_home2():
    return render_template('homepage2.html')


@app.route('/add', methods=['GET'])
def show_add():
    return render_template('add_document.html')


@app.route('/pdf_document/<string:filename>', methods=['GET'])
def get_pdf(filename):
    # https://gist.github.com/jessejlt/1306827 for tips on downloadable PDFs
    return app.send_static_file('pdf/' + filename)


@app.route('/document/<int:docid>', methods=['GET'])
def getdocument(docid):
    doc_data = document_logic.get_document(docid)
    if doc_data:
        return render_template(
            'view_document.html',
            document_data=doc_data)
    else:
        return None


@app.route('/document/search', methods=['GET'])
def search():
    search_string = request.args.get('query')
    return jsonify(search_documents(search_string))


@app.route('/document/ingest', methods=['POST'])
def ingest_document():
    doc_data = request.form
    new_doc_id = unverified_document_logic.add_document(
        doc_data['title'], doc_data['topic_id'], doc_data['content'],
        doc_data['original_url'], doc_data['source']
    )
    return jsonify({'id': new_doc_id})


@app.route('/document/add', methods=['POST'])
def add_document():
    doc_data = request.form
    new_doc_id = document_logic.add_document(
        doc_data['title'], doc_data['topic_id'], doc_data['content'],
        doc_data['original_url'], doc_data['source']
    )
    return jsonify({'id': new_doc_id})


@app.route('/popular', methods=['GET'])
def popular():
    return jsonify([
        {'title': 'List of somethings for 2016', 'id': 2},
        {'title': 'List of something elses for 2015', 'id': 5},
        {'title': 'Goings on for XYZ', 'id': 9},
        {'title': 'Proceedings of the Society for P.T.O.T.O.T', 'id': 13},
        {'title': 'Whos Who of What', 'id': 10},
    ])
