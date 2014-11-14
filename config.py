import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'not_a_secret'
    CELERY_BROKER_URL = "sqla+sqlite:///celerydb.sqlite"
    #CELERY_BROKER_URL='redis://localhost:6379/0'
    #CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
