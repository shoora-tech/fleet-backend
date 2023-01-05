from datetime import timedelta

from celery.schedules import crontab
# from django.utils.dateparse import parse_time
from environ import Env

# NOTE: These settings are read directly from the environment since importing Django
# settings causes a recursive import error.

ENV = Env()

DEFAULT = {
    "calculate-alerts": {
        "task": "alert.tasks.fetch_alerts",
        'schedule': crontab(minute='*/10'),
    },
    "calculate-trips": {
        "task": "trip.tasks.calculate_trips",
        'schedule': crontab(minute='*/10'),
    },
    "calculate-jsession": {
        "task": "device.tasks.update_jsession",
        'schedule': crontab(hour='*/5'),
    },
}
