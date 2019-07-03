from werkzeug.security import generate_password_hash, check_password_hash


class Password(object):

    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def is_password_correct(hash_password:str, password:str):
        return check_password_hash(hash_password, password)