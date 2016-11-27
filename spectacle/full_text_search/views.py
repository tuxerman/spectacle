# -*- coding: UTF-8 -*-
"""
Full text search views
"""
from application import application
from flask import request, jsonify
import spectacle.full_text_search.logic as fts_logic


@application.route('/document/search', methods=['GET'])
def search():
    search_string = request.args.get('query')
    return jsonify(fts_logic.search_documents(search_string))
