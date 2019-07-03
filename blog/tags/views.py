from flask import Blueprint, render_template, request

from blog.models import Post, Tag

blog_tag_app = Blueprint('blog_tag_app', __name__)
POST_PER_PAGE = 15


@blog_tag_app.route("/tags/<tag>")
def tags(tag):

    tag = Tag.query.filter_by(name=tag).first_or_404()
    page = int(request.values.get('page', '1'))
    posts = tag.posts.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POST_PER_PAGE, False)

    return render_template("blog/tag_posts.html", posts=posts, title='Tag: ' + str(tag), tag=str(tag))
