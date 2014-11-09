from celery import Celery
import settings
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build


def make_celery(app):
    celery = Celery(app.import_name,  broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def initialize_service():
    '''initalizes google analytics service'''
    client_email = '556009582678-d1er91t08n95fg8ldvaojdric02pqd8u@developer.gserviceaccount.com'
    with open("ramirez_key.p12") as f:
      private_key = f.read()
    credentials = SignedJwtAssertionCredentials(client_email, private_key,
        'https://www.googleapis.com/auth/analytics.readonly')
    http_auth = credentials.authorize(Http())

    return build('analytics', 'v3', http=http_auth)
