from flask import Blueprint, render_template, request

from blog.models import Post


blog_app = Blueprint('blog_app', __name__)
POST_PER_PAGE = 15

@blog_app.route("/")
def index():

    page = int(request.values.get('page', '1'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POST_PER_PAGE, False)
    return render_template("blog/index.html", posts=posts, title='Latest Posts')

