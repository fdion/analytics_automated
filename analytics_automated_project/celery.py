from __future__ import absolute_import

import os
import time

from celery import Celery
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics_automated_project.settings.dev')


# logger = get_task_logger(__name__)
app = Celery('backend_tasks')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
