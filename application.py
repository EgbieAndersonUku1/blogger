from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown


db = SQLAlchemy()

def create_app(**config_overrides):

    app = Flask(__name__)

    # load config
    app.config.from_pyfile('settings.py')

    # initialize the db
    db.init_app(app)
    Migrate(app, db)
    Markdown(app)

    # imprt blueprints
    from author.login.views import author_login_app
    from author.registration.views import author_registration_app
    from author.logout.views import author_logout_app
    from blog.tags.views import blog_tag_app
    from blog.posts.views import blog_post_app
    from blog.categories.views import blog_categories_app
    from blog.modify.views import blog_modifier_app
    from blog.articles.views import blog_articles_app
    from blog.views import blog_app


    # register blue prints
    app.register_blueprint(author_login_app)
    app.register_blueprint(author_registration_app)
    app.register_blueprint(blog_tag_app)
    app.register_blueprint(author_logout_app)
    app.register_blueprint(blog_categories_app)
    app.register_blueprint(blog_modifier_app)
    app.register_blueprint(blog_post_app)
    app.register_blueprint(blog_articles_app)
    app.register_blueprint(blog_app)


    return app