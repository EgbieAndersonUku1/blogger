from flask import Blueprint, flash

from author import constants

from utils.security.flask_session import Session
from utils.security.secure_redirect import url_secure_redirect


author_logout_app = Blueprint('author_logout_app', __name__)


@author_logout_app.route("/logout")
def logout():
    """"""
    Session.clear_all()
    flash(constants.LOGOUT_MSG)
    return url_secure_redirect("author_login_app.login")