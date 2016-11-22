# -*- coding: UTF-8 -*-
"""
ORM and data functions for User
"""
import md5

from peewee import CharField, DateTimeField, TextField, BooleanField
from datetime import datetime
from flask_login import UserMixin
from app import app, login_serializer

from spectacle.database_definitions import CURRENT_BASE_MODEL


class User(CURRENT_BASE_MODEL, UserMixin):
    username = CharField(primary_key=True, unique=True)
    password_hash = TextField()
    email = CharField()
    verified = BooleanField()
    is_moderator = BooleanField()
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
    try:
        return User.get(User.username == userid)
    except User.DoesNotExist:
        return None


def db_add_user(username, password_hash, email):
    User.create(
        username=username,
        password_hash=password_hash,
        email=email,
        verified=False,
        is_moderator=False,
        date_added=datetime.now(),
    )


def db_promote_user(username):
    user = User.get(username=username)
    if not user:
        raise
    user.is_moderator = True
    user.save()


def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()
