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

app = Flask(__name__)
app.config['DEBUG'] = False

app.config['SECRET_KEY'] = 'TODOsomeprivateflaskstringhere'
app.config['STORMPATH_API_KEY_FILE'] = '.spectacle_apikey'
app.config['STORMPATH_APPLICATION'] = 'spectacle'

app.config.from_object(__name__)

app.secret_key = "a_random_secret_key_$%#!@"
# Login_serializer used to encryt and decrypt the cookie token for the remember
# me option of flask-login
login_serializer = URLSafeTimedSerializer(app.secret_key)

# Flask-Login Login Manager
login_manager = LoginManager()


app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)

# Tell the login manager where to redirect users to display the login page
login_manager.login_view = "/login/"
# Setup the login manager.
login_manager.setup_app(app)
