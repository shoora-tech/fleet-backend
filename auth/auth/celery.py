import os

# from celery import Celery

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth.settings")

app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.task_routes = {
    "alert.tasks.fetch_alerts": {"queue": "scheduling"},
    "trip.tasks.calculate_trips": {"queue": "scheduling"},
    "device.tasks.update_jsession": {"queue": "scheduling"},
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
