from django.contrib.auth.hashers import make_password,check_password

class HashPassword:

    @staticmethod
    def createPassword(password):
        return make_password(password, None, 'pbkdf2_sha256')

    @staticmethod
    def isValidPassword(password,hashPasswd):
        return check_password(password, hashPasswd)