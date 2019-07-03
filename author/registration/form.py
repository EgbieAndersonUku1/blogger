from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from author.models import Author


class RegisterForm(FlaskForm):

    full_name = StringField("Full name", validators=[validators.DataRequired()])
    email = EmailField('Email address', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', validators=[validators.DataRequired(),
                                                         validators.Length(min=4, max=80),
                                                         validators.EqualTo("confirm", message="Password must match")])
    confirm = PasswordField("Repeat Password")


    def validate_form(self, email):

        author = Author.query.filter_by(email=email.data).first()

        if author is not None:
            raise ValidationError("The email is already in use, please use a different email address")