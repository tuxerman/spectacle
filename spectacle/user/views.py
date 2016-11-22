# -*- coding: UTF-8 -*-
"""
Views related to users, logins, sessions, etc.
"""
from flask import flash, jsonify, render_template, request
from app import app
from flask_login import login_required, current_user, login_user, logout_user, redirect
from spectacle.user.model import hash_pass, db_get_user
from spectacle.user.utils import get_current_user_info
from app import login_serializer, login_manager


@app.route("/logout/")
def logout_page():
    """
    Web Page to Logout User, then Redirect them to Index Page.
    """
    logout_user()
    flash('Logged out.')
    return redirect("/")


@app.route("/login/", methods=["GET", "POST"])
def login_page():
    """
    Web Page to Display Login Form and process form.
    """
    if request.method == "POST":
        user = db_get_user(request.form['username'])

        # If we found a user based on username then compare that the submitted
        # password matches the password in the database.  The password is stored
        # is a slated hash format, so you must hash the password before comparing
        # it.
        if user and hash_pass(request.form['password']) == user.password_hash:
            login_user(user, remember=True)
            return redirect(request.args.get("next") or "/")
        flash('Credentials not correct. Try again')

    return render_template("login.html", user_info=get_current_user_info())


@app.route("/restricted/")
@login_required
def restricted_page():
    """
    web page which is restricted and requires the user to be logged in.
    """
    # this is just to display the username in the template not required as part
    # of any Flask-Login requirements.
    user_id = (current_user.get_id() or "No User Logged In")
    return jsonify({'restricted': True, 'user_id': user_id})


@login_manager.user_loader
def load_user(userid):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return
    None based on the userid.
    The userid was stored in the session environment by Flask-Login.
    user_loader stores the returned User object in current_user during every
    flask request.
    """
    return db_get_user(userid)


@login_manager.token_loader
def load_token(token):
    """
    Flask-Login token_loader callback.
    The token_loader function asks this function to take the token that was
    stored on the users computer process it to check if its valid and then
    return a User Object if its valid or None if its not valid.
    """

    # The Token itself was generated by User.get_auth_token.  So it is up to
    # us to known the format of the token data itself.

    # The Token was encrypted using itsdangerous.URLSafeTimedSerializer which
    # allows us to have a max_age on the token itself.  When the cookie is stored
    # on the users computer it also has a exipry date, but could be changed by
    # the user, so this feature allows us to enforce the exipry date of the token
    # server side and not rely on the users cookie to exipre.
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    # Decrypt the Security Token, data = [username, hashpass]
    username, password_hash = login_serializer.loads(token, max_age=max_age)

    # Find the User
    user = db_get_user(username)

    # Check Password and return user or None
    if user and password_hash == user.password_hash:
        return user
    return None
