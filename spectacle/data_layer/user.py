# -*- coding: UTF-8 -*-
"""
ORM and data functions for User
"""
import md5

from peewee import CharField, DateTimeField, TextField, BooleanField
from datetime import datetime
from flask_login import UserMixin
from app import app, login_serializer

from spectacle.data_layer.database_definitions import CURRENT_BASE_MODEL


class User(CURRENT_BASE_MODEL, UserMixin):
    username = CharField(primary_key=True, unique=True)
    password_hash = TextField()
    verified = BooleanField()
    date_added = DateTimeField()

    class Meta:
        order_by = ('date_added',)

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.username), self.password_hash]
        return login_serializer.dumps(data)


def db_get_user(userid):
    """
    Static method to search the database and see if userid exists.  If it
    does exist then return a User Object.  If not then return None as
    required by Flask-Login.
    """
    # For this example the USERS database is a list consisting of
    # (user,hased_password) of users
    return User.get(User.username == userid)


def db_add_user(username, password_hash):
    User.create(
        username=username,
        password_hash=password_hash,
        verified=False,
        date_added=datetime.now(),
    )


def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()
