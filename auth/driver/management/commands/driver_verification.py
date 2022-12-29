from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll
from alert.models import RealTimeDatabase
from trip.models import Trips
import boto3
from environ import Env
from django.conf import settings
import json
import redis
from datetime import datetime, timedelta
from geopy.distance import geodesic
from vehicle.models import Vehicle
import pytz
import requests
import urllib.parse
from device.models import Device
from driver.models import Driver
from auth.face_recognizer import compare_face_by_url

# redis storage
r = redis.Redis(
    host='redis',
    port=6379, 
    db=0,
    charset="utf-8",
    decode_responses=True
    )

# sqs = boto3.client('sqs')
sqs = boto3.client('sqs',
        region_name="ap-south-1",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


class Command(BaseCommand):
    help = 'Pulls SQS data and push it to RealtimeDatabase'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def change_case(self, str):
        return ''.join(['_'+i.lower() if i.isupper()
                else i for i in str]).lstrip('_')
    
    def format_sqs_data(self, data):
        x = {}
        for key, value in data.items():
            x[self.change_case(key)] = value
        
        return x
    
    def get_gps_for_corrupt_data(self, imei, last_stored_point, corrupted_point):
        try:
            temp = RealTimeDatabase.objects.filter(imei=imei, is_corrupt=False,id__gte=last_stored_point, id__lte=corrupted_point)
            if temp:
                temp = temp.last()
                valid_cordinates = {}
                valid_cordinates['latitude'] = temp.latitude
                valid_cordinates['longitude'] = temp.longitude
                return valid_cordinates
            return None
        except RealTimeDatabase.DoesNotExist:
            return None
    
    def capture_image(self, device_id):
        print("dev id ", device_id)
        driver_img_capture_url = "http://dsm.shoora.com/StandardApiAction_capturePicture.action"
        capture_params = {
            "jsession": "02d011cfea1840cea9f98a4b4e5d8589",
            "Type": 1,
            "DevIDNO": device_id,
            "Chn": 1
        }
        # url = "http://dsm.shoora.com/StandardApiAction_capturePicture.action?jsession=02d011cfea1840cea9f98a4b4e5d8589&Type=1&DevIDNO=784087664080&Chn=1"
        resp = requests.get(url=driver_img_capture_url, params=capture_params)
        print("resp is ", resp)
        data = resp.json()
        print("data is ", data)
        flength = data['FLENGTH']
        foffset = data['FOFFSET']
        fpath = data['FPATH']
        # fpath = fpath.replace('\\', '\\\\')
        print("fpath is ", data['FPATH'])
        image_params = {
            "FLENGTH": flength,
            "FOFFSET": foffset,
            "FPATH": fpath,
            "MTYPE": 1,
            "SAVENAME": device_id,
            "TYPE": 3
        }
        image_url = "http://dsm.shoora.com:6611/3/5?"
        image_url = image_url + f'Type=3&FLENGTH={flength}&FOFFSET={foffset}&FPATH={fpath}&MTYPE=1&SAVENAME={device_id}'
        # for key, val in image_params.items():
        #     image_url+
        # image_url = image_url + urllib.parse.urlencode(image_params)
        # image_url = urllib.parse.unquote(image_url)
        # image_url = "http://dsm.shoora.com:6611/3/5?Type=3&FLENGTH=199863&FOFFSET=318896&FPATH=E:\\gStorage\\STOMEDIA\\2022-12-25\\20221225-155922_SS1.picfile&MTYPE=1&SAVENAME=downImage"
        return image_url



    # @shared_task
    def driver_verification(self):
        print("doing driver verification")
        # get all current on-going trips and capture image for those which has just started
        # ongoing_trips_imei = r.hgetall('trips')
        ongoing_trips_imei = r.lrange("trips", 0, -1)
        print("ongoing trips ", ongoing_trips_imei)
        for imei in ongoing_trips_imei:
            # picture_imei = r.hgetall(imei)
            unknown_image_url = self.capture_image(imei)
            # get list of known images url
            device = Device.objects.get(imei_number=imei)
            org = device.organization
            drivers = Driver.objects.filter(organization=org)
            known_image_urls = []
            for driver in drivers:
                if driver.image:
                    known_image_urls.append(driver.image.url)
            print("driver image urls ", known_image_urls)
            proceed, flag, pos = compare_face_by_url(known_image_urls, unknown_image_url)
            print(f'Proceed = {proceed} , Flag = {flag} , pos = {pos}')
            if proceed:
                if flag:
                    # print which driver it is
                    print("driver image is ", known_image_urls[pos])


        # check the imeis for which photos have been taken and start taking pics
        pictures_imei = r.hgetall('pictures')

    def handle(self, *args, **options):
        # fetch realtime data from last stored point
        self.driver_verification()
            