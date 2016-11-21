# -*- coding: UTF-8 -*-
"""
Full text search views
"""
from app import app
from flask import request, jsonify
import spectacle.full_text_search.logic as fts_logic


@app.route('/document/search', methods=['GET'])
def search():
    search_string = request.args.get('query')
    return jsonify(fts_logic.search_documents(search_string))
