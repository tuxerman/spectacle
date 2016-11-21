# -*- coding: UTF-8 -*-
"""
Helper functions related to users, logins, sessions, etc.
"""
from functools import wraps

from flask_login import current_user
from flask_login import redirect


def get_current_user_info():
    user_info = {'logged_in': False, 'user_id': None, 'is_moderator': False}
    if current_user.is_authenticated:
        user_info['username'] = current_user.username
        user_info['logged_in'] = True
        user_info['is_moderator'] = current_user.is_moderator
    return user_info


def moderators_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_moderator:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper
