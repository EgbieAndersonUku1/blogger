from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, validators, TextAreaField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from blog.models import Category


def categories():
    return Category.query


class PostForm(FlaskForm):

    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], "We only accept JPG and PNG")])
    title = StringField('Title', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    body = TextAreaField('Content', validators=[validators.DataRequired()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category = StringField('New Category')