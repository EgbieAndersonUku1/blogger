from flask import Blueprint, render_template

from blog.models import Post


blog_articles_app = Blueprint("blog_articles_app", __name__)

@blog_articles_app.route('/posts/all/<slug>')
def articles(slug):

    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/articles.html', post=post)