import os

class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = 'not_a_secret'
    CLIENT_EMAIL = '556009582678-d1er91t08n95fg8ldvaojdric02pqd8u@developer.gserviceaccount.com'
    GA_P12_KEY = 'secret_key.p12'
    CELERY_BROKER_URL =  "sqla+sqlite:///celerydb.sqlite"
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
