import os
import unittest
import pathlib

from author import constants
from utils.security.flask_session import Session


from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))

from author.models import AuthorDB
from application import db
from application import create_app as create_app_base
from utils.test_db import TestDB


class AuthorTest(unittest.TestCase):

    def create_app(self):
        return create_app_base(
            SQLALCHEMY_DATABASE_URL=self.db_uri,
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='mySecret'
        )

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()
        self.test_db.drop_db()

    def user_dict(self):
        return dict(
            full_name='Egbie Anderson',
            email="egbie@example.com",
            password="password123",
            confirm="password123"
        )

    def test_user_register(self):

        # check user registration
        rv = self.app.post("/register", data=self.user_dict(), follow_redirects=True)
        assert constants.REGISTRATION_SUCCESSFUL in str(rv.data)

        with self.app as c:
            rv = c.get("/")
            assert AuthorDB.query.filter_by(email=self.user_dict()['email']).count() == 1

    def test_user_login(self):

        rv = self.app.post("/register", data=self.user_dict(), follow_redirects=True)

        with self.app as c:
            rv = c.post("/login", data=self.user_dict(), follow_redirects=True)
            assert Session.get_session_by_id() == 1

    


