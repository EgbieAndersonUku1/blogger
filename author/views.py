from flask import Blueprint, render_template, flash, request

from application import db
from author import constants
from author.forms.login.form import LoginForm
from author.forms.registration.form import RegisterForm
from author.models import Author
from utils.security.password import Password
from utils.security.flask_session import Session
from utils.security.secure_redirect import url_secure_redirect


author_app = Blueprint('author_app', __name__)


@author_app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        author = Author(form.full_name.data,
                          form.email.data,
                          password=Password.generate_password_hash(form.password.data)
                          )
        db.session.add(author)
        db.session.commit()
        flash(constants.REGISTRATION_SUCCESSFUL)
        return url_secure_redirect("author_app.login")
    return render_template('author/register.html', form=form)


@author_app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    error = None

    if request.method == "GET" and request.args.get("next"):
        Session.add(key="next", value=request.args.get("next"))
    if form.validate_on_submit():

        author = Author.query.filter_by(email=form.email.data.lower()).first()
        _add_user_details_to_session(author)

        next = Session.get("next")
        return url_secure_redirect('blog_app.post', next) if next else url_secure_redirect("blog_app.index")

    return render_template("author/login.html", form=form, error=error)


@author_app.route("/logout")
def logout():
    """"""
    Session.clear_all()
    flash(constants.LOGOUT_MSG)
    return url_secure_redirect("author_app.login")


def _add_user_details_to_session(author):

    Session.add('id', author.id)
    Session.add('email', author.email)
    Session.add('full_name', author.full_name)
