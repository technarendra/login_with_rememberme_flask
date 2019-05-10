import os
from datetime import timedelta

#application directory
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # DB_CONFIG = {
    #     'host': 'localhost',
    #     'port': '5432',
    #     'database': 'postgres',
    #     'user': 'postgres',
    #     'password': 'p05tgre5',
    # }

    # class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://///home/narendra/narendra/flask/flaskloginRemembup/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    #secret key for signing the data. 
    CSRF_SESSION_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "thisissecretkey"

    USER_ENABLE_EMAIL = False

    USE_SESSION_FOR_NEXT = True

    REMEMBER_COOKIE_DURATION = timedelta(seconds=90)