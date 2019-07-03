from slugify import slugify
from flask import Blueprint, render_template, flash, redirect, url_for, request

from application import db
from blog import constants
from blog.form import PostForm
from author.models import Author
from blog.models import Post, Category, Tag

from utils.security.flask_session import Session
from utils.imager import Imager, ImageSize

from utils.security.secure_redirect import is_safe_url
from utils.security.secure_upload import secure_image_uploader
from settings import BLOG_POST_IMAGES_PATH
from author.decorator import login_required


blog_post_app = Blueprint("blog_post_app", __name__)


@blog_post_app.route("/post", methods=["GET", "POST"])
@login_required
def post():

    form = PostForm()
    tags_field = request.values.get("tags_field", '')

    if form.validate_on_submit():
        image_id = None

        if form.image.data:
            file_path, img_id = secure_image_uploader(form, file_path=BLOG_POST_IMAGES_PATH)
            _resize_post_image_for_home_page_and_post_page(file_path, img_id)
            image_id = img_id

        category = _get_form_category_data(form)

        author = Author.query.get(Session.get_session_by_id())
        title, body = _get_data_from_form(form)

        post = Post(author=author, title=title, body=body, image=image_id, category=category)
        _save_tag(post, tags_field)
        db.session.add(post)
        db.session.commit()

        slug = _gen_slug_from_post(post)
        flash(constants.ARTICLE_POSTED_MSG)

        if is_safe_url('blog_app.article'):
            return redirect(url_for('blog_app.articles', slug=slug))
    return render_template("blog/post.html", form=form, action="new")


def _resize_post_image_for_home_page_and_post_page(file_path, image_id):

    img = Imager(file_path, image_id, ImageSize.SIX_HUNDRED_PIXELS) # for post page
    img.resize()
    img.img_size = ImageSize.THREE_HUNDRED_PIXELS  # for home page
    img.resize()


def _get_form_category_data(form):

    if form.new_category.data:
        new_category = Category(form.new_category.data)
        db.session.add(new_category)
        db.session.flush()
        category = new_category
    else:
        category = form.category.data
    return category


def _get_data_from_form(form):
    title = form.title.data.strip()
    body = form.body.data.strip()
    return title, body


def _gen_slug_from_post(post):
    slug = slugify(str(post.id) + "_" + post.title)
    post.slug = slug
    db.session.commit()
    return slug


def _save_tag(post, tags_field):
    post.tags.clear()

    for tag_item in tags_field.strip().split(","):
        tag = Tag.query.filter_by(name=slugify(tag_item)).first()

        if not tag:
            tag = Tag(name=slugify(tag_item))
            db.session.add(tag)
        post.tags.append(tag)
    return post
