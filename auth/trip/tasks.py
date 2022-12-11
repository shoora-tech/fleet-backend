from celery import shared_task
from alert.models import RealTimeDatabase

@shared_task
def calculate_trips():
    print("Hello there!")
    # fetch data from the last saved realtimedata id
    last_saved_id = 1
    rtd = RealTimeDatabase.objects.filter(id__gt=last_saved_id)
    