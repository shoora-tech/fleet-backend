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
from django.utils import timezone

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
            temp = RealTimeDatabase.objects.filter(imei=imei, longitude__lt=90,id__gte=last_stored_point, id__lte=corrupted_point)
            if temp:
                temp = temp.last()
                valid_cordinates = {}
                valid_cordinates['latitude'] = temp.latitude
                valid_cordinates['longitude'] = temp.longitude
                return valid_cordinates
            return None
        except RealTimeDatabase.DoesNotExist:
            return None

    def handle(self, *args, **options):
        # fetch realtime data from last stored point
        last_stored_point = r.get("realtime_last_stored_point")
        # for each device check if status is ignition Off and device id stored in Redis
        # mark that trip as complete and save in db
        if last_stored_point:

            last_stored_point = int(last_stored_point)
            rtd = RealTimeDatabase.objects.filter(id__gte=last_stored_point).values(
                "id",
                "imei",
                "ignition_status",
                "latitude",
                "longitude",
                "speed",
                "created_at",
                "is_corrupt",
            )
            new_id = None
            for rt in rtd:
                status = rt['ignition_status']
                latitude = rt['latitude']
                longitude = rt['longitude']
                created_at = rt['created_at']
                is_corrupt = rt['is_corrupt']
                imei_data = r.hgetall(str(rt['imei']))
                # if longitude > 90:
                #     is_corrupt = True
                
                if imei_data and len(imei_data)>0:
                    if not status and is_corrupt==False:
                        # mark trip as end and store this trip and remove this key from redis
                        # if is_corrupt:
                        #     valid_cordinates = self.get_gps_for_corrupt_data(rt['imei'], last_stored_point, rt['id'])
                        #     if not valid_cordinates:
                        #         continue
                        #     latitude = valid_cordinates['latitude']
                        #     longitude = valid_cordinates['longitude']
                        start_pos = (imei_data['latitude'], imei_data['longitude'])
                        end_pos = (latitude, longitude)
                        try:
                            vehicle = Vehicle.objects.get(device__imei_number=rt['imei'])
                            driver = vehicle.driver.first()
                            t1 = datetime.strptime(str(imei_data['started_at']), "%y-%m-%dT%H:%M:%S")
                            t1 = t1.replace(tzinfo=pytz.UTC)
                            duration = (created_at - t1).total_seconds()
                            gps_end=None
                            gps_start = imei_data.get('id', None)
                            if gps_start:
                                gps_end=rt['id']
                            if duration < 0:
                                duration = 0 - duration
                            distance = geodesic(start_pos, end_pos).km
                            if distance >= 5:
                                trip = Trips.objects.create(
                                        start_latitude=str(imei_data['latitude']),
                                        start_longitude=str(imei_data['longitude']),
                                        end_latitude=latitude,
                                        end_longitude=longitude,
                                        started_at=t1,
                                        ended_at=created_at,
                                        distance=geodesic(start_pos, end_pos).km,
                                        duration=duration,
                                        driver=driver,
                                        vehicle=vehicle,
                                        gps_end=gps_end,
                                        gps_start=gps_start
                                    )
                                # print("trip created --> ", trip)
                            r.delete(str(rt['imei']))
                        except Vehicle.DoesNotExist:
                            r.delete(str(rt['imei']))
                else:
                    if status and not imei_data and not is_corrupt:
                        # print("setting data ..")
                        # set imei data in redis
                        data = {
                            "id": rt['id'],
                            "latitude": latitude,
                            "longitude": longitude,
                            "started_at": datetime.strftime(created_at, "%y-%m-%dT%H:%M:%S")
                        }
                        r.hmset(str(rt['imei']), data)
                # print("imei_data ", imei_data)
                new_id = rt['id']
            if new_id:
                r.set("realtime_last_stored_point", new_id)
        else:
            now = timezone.now()
            now_minus_1 = now - timedelta(minutes = 10)
            rtd = RealTimeDatabase.objects.filter(created_at__gte=now_minus_1).values(
                "id",
                "imei",
                "ignition_status",
                "latitude",
                "longitude",
                "speed",
                "is_corrupt",
                "created_at",
            )
            new_id = None
            
            for rt in rtd:
                status = rt['ignition_status']
                latitude = rt['latitude']
                longitude = rt['longitude']
                created_at = rt['created_at']
                imei_data = r.hgetall(str(rt['imei']))
                # print("imei data ", imei_data)
                # print("json data ", type(imei_data))
                if status and not imei_data:
                # set imei data in redis
                    data = {
                        "id": rt['id'],
                        "latitude": latitude,
                        "longitude": longitude,
                        "started_at": datetime.strftime(created_at, "%y-%m-%dT%H:%M:%S")
                    }
                    r.hmset(str(rt['imei']), data)
                
                new_id = rt['id']
            if new_id:
                r.set("realtime_last_stored_point", new_id)
            