from celery import shared_task
from alert.models import RealTimeDatabase
from django.core.management import call_command


@shared_task
def calculate_trips():
    call_command('trip')
    