import os, ssl

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_snippets.settings")

app = Celery("django_snippets",
             broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     },
     redis_backend_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     }
             )

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(settings.INSTALLED_APPS)
