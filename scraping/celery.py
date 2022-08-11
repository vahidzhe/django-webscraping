from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraping.settings')


app = Celery('proj')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


from celery.schedules import crontab  # scheduler

# scheduled task execution
app.conf.beat_schedule = {
    # executes every 1 minute
    "scraping-task-five-min": {
        "task": "product.tasks.scapy",
         "schedule": crontab(minute=21, hour="*/1")
         }
}




@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
