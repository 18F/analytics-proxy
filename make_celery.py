from celery import Celery
from sqlalchemy import *

def make_celery(app):
    celery = Celery(app.import_name, broker='sqla+sqlite:///celerydb.sqlite')
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
