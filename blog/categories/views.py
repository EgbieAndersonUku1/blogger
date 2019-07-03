from flask import Blueprint, render_template, request

from blog.models import Post, Category

POST_PER_PAGE = 15

blog_categories_app = Blueprint('blog_categories_app', __name__)


@blog_categories_app.route("/categories/<category_id>")
def categories(category_id):

    category = Category.query.filter_by(id=category_id).first_or_404()
    page = int(request.values.get('page', '1'))
    posts = Post.query.filter_by(category=category, live=True).\
        order_by(Post.publish_date.desc()).paginate(page, POST_PER_PAGE, False)

    return render_template("blog/category_posts.html", posts=posts, title=category, category_id=category_id)