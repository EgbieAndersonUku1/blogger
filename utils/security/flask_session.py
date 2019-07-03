from flask import session


class Session(object):

    @staticmethod
    def add(key, value):
        session[key] = value

    @staticmethod
    def get_session_by_email():
        return session.get("email")

    @staticmethod
    def get_session_by_id():
        return session.get("id")

    @staticmethod
    def clear_all():
        session.clear()

    @staticmethod
    def get(key):
        return session.get(key)


