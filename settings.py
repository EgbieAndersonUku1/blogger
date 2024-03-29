import os

SECRET_KEY = os.environ['SECRET_KEY']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DATABASE_NAME = os.environ['DATABASE_NAME']

# mysql+pymsql://username:password@host:3306/databasename
DB_URI = "mysql+pymysql://%s:%s@%s:3306/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
MYSQL_ROOT_PASSWORD = os.environ['MYSQL_ROOT_PASSWORD']
BLOG_NAME = os.environ['BLOG_NAME']
BLOG_POST_IMAGES_PATH = os.environ['BLOG_POST_IMAGES_PATH']
SQLALCHEMY_TRACK_MODIFICATIONS=False