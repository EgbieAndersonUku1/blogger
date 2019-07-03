from flask import Blueprint, render_template, flash, redirect, url_for
from slugify import slugify

from application import db
from author.decorator import login_required
from blog import constants
from blog.models import Post, Category
from blog.form import PostForm
from utils.imager import ImageSize
from utils.security.secure_redirect import is_safe_url
from utils.security.secure_upload import secure_image_uploader
from utils.imager import resize_post_image
from settings import BLOG_POST_IMAGES_PATH


blog_modifier_app = Blueprint("blog_modifier_app", __name__)


@blog_modifier_app.route("/edit/<slug>", methods=["GET", "POST"])
@login_required
def edit(slug):

    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)

    if form.validate_on_submit():

        original_img_id, original_title = post.image, post.title
        form.populate_obj(post)

        post.image = _if_image_is_found_process_image(form, original_img_id)
        _if_new_category_is_found_process(form, post)
        _if_post_title_has_changed_slugify(form, post, original_title)

        db.session.commit()

        flash(constants.ARTICLE_EDITED_MSG)

        if is_safe_url('blog_articles_app.articles'):
            return redirect(url_for('blog_articles_app.articles', slug=post.slug))

    return render_template("blog/post.html", form=form, post=post, action="edit")


@blog_modifier_app.route("/delete/<slug>")
@login_required
def delete(slug):

    post = Post.query.filter_by(slug=slug).first_or_404()
    post.live = False
    db.session.commit()

    flash(constants.ARTICLE_DELETED_MSG)

    if is_safe_url('blog_app.index'):
        return redirect(url_for('blog_app.index', slug=slug))


def _if_image_is_found_process_image(form, original_image_id):

    image_id = original_image_id

    if form.image.data:
        file_path, img_id = secure_image_uploader(form, file_path=BLOG_POST_IMAGES_PATH)
        resize_post_image(file_path, img_id, ImageSize.SIX_HUNDRED_PIXELS) # for post page
        resize_post_image(file_path, img_id, ImageSize.THREE_HUNDRED_PIXELS) # for home page
        image_id = img_id
    return image_id


def _if_new_category_is_found_process(form, post):

    if form.new_category.data:
        new_category = Category(form.new_category.data)
        db.session.add(new_category)
        db.session.flush()
        post.category = new_category


def _if_post_title_has_changed_slugify(form, post, original_title):

    if form.title.data != original_title:
        post.slug = slugify(str(post.id) + "-" + form.title.data)
