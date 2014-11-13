from celery.schedules import crontab

#schedules the data to be collected every hour
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.process_analytics',
        'schedule': crontab(minute='*/1'),#crontab(minute=0, hour='*/1'), #
        'args': (),
    },
}
