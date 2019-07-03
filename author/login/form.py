from flask_wtf import FlaskForm
from wtforms import PasswordField, validators
from wtforms.fields.html5 import EmailField

from author.models import Author
from utils.security.password import Password
from author import errors


class LoginForm(FlaskForm):

    email = EmailField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.Length(min=8, max=80)])

    def validate(self):

        rv = FlaskForm.validate(self)
        if not rv:
            return False

        author = self._get_user_email()

        if author and Password.is_password_correct(hash_password=author.password, password=self.password.data):
            return True
        self.password.errors.append(errors.INCORRECT_CREDENTIALS)
        return False

    def _get_user_email(self):
        return Author.query.filter_by(email=self.email.data).first()


