import os


class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Default Key'
    CLIENT_EMAIL = os.getenv('CLIENT_EMAIL')
    GA_P12_KEY = os.getenv('GA_P12_KEY')
    REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'


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
