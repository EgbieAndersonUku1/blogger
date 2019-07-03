from flask import Blueprint, render_template, flash

from application import db
from author import constants

from author.registration.form import RegisterForm
from author.models import Author
from utils.security.password import Password
from utils.security.secure_redirect import url_secure_redirect

author_registration_app = Blueprint('author_registration_app', __name__)


@author_registration_app.route("/register", methods=['GET', 'POST'])
def register():
    """Allows the user of the application to register"""

    form = RegisterForm()

    if form.validate_on_submit():
        author = Author(form.full_name.data,
                          form.email.data,
                          password=Password.generate_password_hash(form.password.data)
                          )
        db.session.add(author)
        db.session.commit()

        flash(constants.REGISTRATION_SUCCESSFUL)
        return url_secure_redirect("author_login_app.login")
    return render_template('author/register.html', form=form)


