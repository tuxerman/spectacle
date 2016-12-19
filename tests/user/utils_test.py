# -*- coding: UTF-8 -*-
"""
Helper functions related to users, logins, sessions, etc.
"""
import md5
from functools import wraps
from application import application
from flask_login import current_user
from flask import redirect


def get_current_user_info():
    user_info = {'logged_in': False, 'username': None, 'is_moderator': False}
    if current_user.is_authenticated:
        user_info['username'] = current_user.username
        user_info['logged_in'] = True
        user_info['is_moderator'] = current_user.is_moderator
    return user_info


def moderators_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_moderator:
            return redirect('/login?reason=mod_access_reqd')
        return func(*args, **kwargs)
    return wrapper


def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    salted_password = password + application.secret_key
    return md5.new(salted_password).hexdigest()
