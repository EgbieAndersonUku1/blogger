from functools import wraps
from flask import flash

from author import constants
from utils.security.flask_session import Session
from utils.security.secure_redirect import url_secure_redirect


def login_required(f):
    @wraps(f)
    def decorated_funcion(*args, **kwargs):

        if Session.get_session_by_id() is None:
            flash(constants.LOGIN_REQUIRED_MSG)
            return url_secure_redirect(url_to_redirect_to="author_login_app.login", go_to_referred_url=True)
        return f(*args, **kwargs)
    return decorated_funcion


def is_user_already_logged_in(f):
    """If the user is already logged in and the user hits /login the application
       the application redirects the user to index page instead of the login page
    """
    @wraps(f)
    def is_user_logged_in(*args, **kwargs):
        if Session.get_session_by_id():
            return url_secure_redirect(url_to_redirect_to="blog_app.index")
        return f(*args, **kwargs)
    return is_user_logged_in
