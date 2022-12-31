from celery import shared_task
from django.conf import settings
import requests
from organization.models import JSession

@shared_task
def update_jsession():
    login_url = settings.JSESSION_URL
    resp = requests.get(url=login_url)
    if resp.status_code == 200:
        # save the jsession id
        data = resp.json()
        obj, created = JSession.objects.update_or_create(jsesion=data['jsession'])


# @shared_task
# def update_jsession():
#     login_url = settings.JSESSION_URL
#     resp = requests.get(url=login_url)
#     if resp.status_code == 200:
#         # save the jsession id
#         data = resp.json()
#         obj, created = JSession.objects.update_or_create(jsesion=data['jsession'])



