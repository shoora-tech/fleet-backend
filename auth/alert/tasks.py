from celery import shared_task
import requests
from alert.models import RawAlert
from datetime import datetime, timedelta
from django.conf import settings
from vehicle.models import Vehicle
from alert.models import Alert
from urllib.parse import urlparse

FORWARD_COLLISION_WARNING = "Forward Collision Warning"
LANE_DEVIATION_WARNING = "Lane Deviation Warning"
CLOSE_CAR_WARNING = "Car Close Distance Warning"
PEDESTRIAN_WARNING = "Pedestrian Detection Warning"
FATIGUE_WARNING = "Fatigue Warning"
MOBILE_USAGE_WARNING = "Mobile Phone Use Warning"
SMOKING_WARNING = "Smoking Warning"
DISTRACTED_DRIVING_WARNING = "Distracted Driving Warning"
UNDETECTED_FACE_WARNING = "Face Not detected Warning"

alarm_name_type_map = {
    601: FORWARD_COLLISION_WARNING,
    603: LANE_DEVIATION_WARNING,
    605: CLOSE_CAR_WARNING,
    607: PEDESTRIAN_WARNING,
    619: FATIGUE_WARNING,
    621: MOBILE_USAGE_WARNING,
    623: SMOKING_WARNING,
    625: DISTRACTED_DRIVING_WARNING,
    627: UNDETECTED_FACE_WARNING
}

@shared_task
def fetch_alerts():
    now = datetime.now()
    now_minus_10 = now - timedelta(minutes = 10)
    raw_alert = RawAlert.objects.filter(updated_at__gte=now_minus_10).values(
        "device_id_no",
        "alert_latitude",
        "alert_longitude",
        "alert_guid",
        "hd",
        "info",
        "img",
        "p1",
        "p2",
        "p3",
        "p4",
        "rve",
        "alert_type_1",
        "alert_type_2",
        "alert_type_3",
        "src_tm",
        "time"
    )
    resp = requests.get(
        url=settings.JSESSION_URL
    )
    if resp.status_code == 200:
        jsession_id = resp.json()["JSESSIONID"]

        for alert in raw_alert:
            # run api to fetch video fr the same
            try:
                print("trying for device ", alert['device_id_no'])
                vehicle = Vehicle.objects.get(device__imei_number=int(alert['device_id_no']))
                driver = vehicle.driver.first()
                params = {
                    "jsession":jsession_id,
                    "begintime":alert['src_tm'],
                    "endtime":alert['time'],
                    "alarmType":",".join([alert['alert_type_1'],alert['alert_type_2'],alert['alert_type_3']]),
                    "mediaType":1,
                    "toMap":2,
                    "vehiIdno":vehicle.vin,
                    "currentPage":1
                }
                video_response = requests.get(url=settings.FETCH_ALARM_VIDEO_URL, params=params)
                if video_response.status_code == 200:
                    infos = video_response.json()['infos']
                    if infos and len(infos) > 0:
                        info = infos[0]
                        file_url = info['fileUrl']
                        parsing = urlparse(file_url)
                        shoora_file_url = parsing._replace(netloc='admin.shoora.com', path='/video'+parsing.path).geturl()
                        alarm_type = info['alarmType']
                        alarm_name = alarm_name_type_map[int(alarm_type)]
                        Alert.objects.create(
                            alert_video_url_china=file_url,
                            alert_video_url_shoora=shoora_file_url,
                            device_imei=info['devIdno'],
                            alert_time_epoch=info['fileSTime'],
                            alarm_type=info['alarmType'],
                            alarm_name=alarm_name,
                            vehicle=vehicle,
                            driver=driver
                            latitude=alert["alert_latitude"],
                            longitude=alert["alert_longitude"],
                            guid=alert["alert_guid"],
                            org=vehicle.organization
                        )
            except Exception as e:
                print("exception --> ", e)






# @shared_task
# def fetch_alerts():
#     print("Hello there!")
#     # get jsession
#     resp = requests.get(
#         url="http://dsm.shoora.com/StandardApiAction_login.action?account=its&password=000000"
#     )
#     if resp.status_code == 200:
#         jsession_id = resp.data["JSESSIONID"]
#         # fetch alerts
#         url = (
#             "http://dsm.shoora.com/StandardApiAction_performanceReportPhotoListSafe.action?jsession="
#             + jsession_id
#             + "&begintime=2022-10-11 00:01:00&endtime=2022-19-11 17:00:00&alarmType=605&mediaType=1&toMap=2&vehiIdno=HR38AC8318&currentPage=1&pageRecords=10"
#         )
#         alert_resp = requests.get(url=url)
#         if alert_resp.status_code == 200:
#             infos = alert_resp.data
#             for info in infos:
#                 print("video_url ", info["fileUrl"])

from django.core.management import call_command
@shared_task
def poll_task():
    call_command('poll')
