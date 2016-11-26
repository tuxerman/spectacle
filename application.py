# -*- coding: UTF-8 -*-
"""
Main app
"""

import os
from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager
from datetime import timedelta

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

application = Flask(__name__)
application.config['DEBUG'] = False
application.config.from_object(__name__)
application.secret_key = "top_secret_keep_hands_off_key_$%#!@"

# Logins and sessions
application.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
login_serializer = URLSafeTimedSerializer(application.secret_key)
login_manager = LoginManager()
login_manager.login_view = "/login/"
login_manager.setup_app(application)
