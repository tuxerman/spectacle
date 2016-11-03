# -*- coding: UTF-8 -*-
"""
Main app
"""

import os
from flask import Flask

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)
