# -*- coding: UTF-8 -*-
"""
Main app
"""

import os
from flask import Flask
from flask.ext.stormpath import StormpathManager


APP_ROOT = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'TODOsomeprivateflaskstringhere'
app.config['STORMPATH_API_KEY_FILE'] = '.spectacle_apikey'
app.config['STORMPATH_APPLICATION'] = 'spectacle'

stormpath_manager = StormpathManager(app)

app.config.from_object(__name__)
