from flask import Blueprint, render_template, request

from author.login.form import LoginForm
from author.models import Author
from utils.security.flask_session import Session
from utils.security.secure_redirect import url_secure_redirect


author_login_app = Blueprint('author_login_app', __name__)


@author_login_app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    error = None

    if request.method == "GET" and request.args.get("next"):
        Session.add(key="next", value=request.args.get("next"))
    if form.validate_on_submit():

        author = Author.query.filter_by(email=form.email.data.lower()).first()
        _add_user_details_to_session(author)

        next = Session.get("next")
        return url_secure_redirect('blog_post_app.post', next) if next else url_secure_redirect("blog_app.index")

    return render_template("author/login.html", form=form, error=error)


def _add_user_details_to_session(author):

    Session.add('id', author.id)
    Session.add('email', author.email)
    Session.add('full_name', author.full_name)