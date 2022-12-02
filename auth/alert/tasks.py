from celery import shared_task
import requests


@shared_task
def hello():
    print("Hello there!")


@shared_task
def fetch_alerts():
    print("Hello there!")
    # get jsession
    resp = requests.get(
        url="http://dsm.shoora.com/StandardApiAction_login.action?account=its&password=000000"
    )
    if resp.status_code == 200:
        jsession_id = resp.data["JSESSIONID"]
        # fetch alerts
        url = (
            "http://dsm.shoora.com/StandardApiAction_performanceReportPhotoListSafe.action?jsession="
            + jsession_id
            + "&begintime=2022-10-11 00:01:00&endtime=2022-19-11 17:00:00&alarmType=605&mediaType=1&toMap=2&vehiIdno=HR38AC8318&currentPage=1&pageRecords=10"
        )
        alert_resp = requests.get(url=url)
        if alert_resp.status_code == 200:
            infos = alert_resp.data
            for info in infos:
                print("video_url ", info["fileUrl"])
