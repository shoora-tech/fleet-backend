from celery import shared_task
from alert.models import RealTimeDatabase
from django.core.management import call_command
import redis
import requests
from device.models import Device
from driver.models import Driver
from auth.face_recognizer import compare_face_by_url

r = redis.Redis(
    host='redis',
    port=6379, 
    db=0,
    charset="utf-8",
    decode_responses=True
    )


# @shared_task
# def calculate_trips():
#     call_command('trip')

def capture_image(device_id):
    url = "http://dsm.shoora.com/StandardApiAction_capturePicture.action?jsession=5e26c72f2f81404c835b637adb372921&Type=1&DevIDNO=784087664080&Chn=1"
    resp = requests.get(url=url)
    data = resp.data
    flength = data['FLENGTH']
    foffset = data['FOFFSET']
    fpath = data['FPATH']
    image_url = "http://dsm.shoora.com:6611/3/5?Type=3&FLENGTH=199863&FOFFSET=318896&FPATH=E:\\gStorage\\STOMEDIA\\2022-12-25\\20221225-155922_SS1.picfile&MTYPE=1&SAVENAME=downImage"
    return image_url



@shared_task
def driver_verification():
    # get all current on-going trips and capture image for those which has just started
    ongoing_trips_imei = r.hgetall('trips')
    for imei in ongoing_trips_imei:
        picture_imei = r.hgetall(imei)
        unknown_image_url = capture_image(picture_imei)
        # get list of known images url
        device = Device.objects.get(imei_number=imei)
        org = device.organization
        drivers = Driver.objects.filter(organization=org)
        known_image_urls = []
        for driver in drivers:
            known_image_urls.append(driver.image.url)
        proceed, flag, pos = compare_face_by_url(known_image_urls, unknown_image_url)
        if proceed:
            if flag:
                # print which driver it is
                print("driver image is ", known_image_urls[pos])


    # check the imeis for which photos have been taken and start taking pics
    pictures_imei = r.hgetall('pictures')

    