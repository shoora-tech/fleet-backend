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

    def handle(self, *args, **options):
        # fetch realtime data from last stored point
        last_stored_point = r.get("realtime_last_stored_point")
        # for each device check if status is ignition Off and device id stored in Redis
        # mark that trip as complete and save in db
        print("last_stored_point --> ", last_stored_point)
        if last_stored_point:
            last_stored_point = int(last_stored_point)
            print("convereted store data ", last_stored_point)
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
                imei_data = r.hgetall(str(rt['imei']))
                print(f"imei data {imei_data} --> {status}")
                # print("json data ", type(imei_data))
                
                if imei_data and len(imei_data)>0:
                    if not status:
                        print("marking trip as complete")
                        # mark trip as end and store this trip and remove this key from redis
                        is_corrupt = rt['is_corrupt']
                        if is_corrupt:
                            # change the end lat, long to a rt which is not corrupt
                            try:
                                rt = RealTimeDatabase.objects.get(imei=rt['imei'], is_corrupt=False,id__gte=last_stored_point, id__lte=rt['id']).values(
                                        "id",
                                        "imei",
                                        "ignition_status",
                                        "latitude",
                                        "longitude",
                                        "speed",
                                        "created_at",
                                        "is_corrupt",
                                    )
                            except RealTimeDatabase.DoesNotExist:
                                continue
                        start_pos = (imei_data['latitude'], imei_data['longitude'])
                        end_pos = (latitude, longitude)
                        try:
                            vehicle = Vehicle.objects.get(device__imei_number=rt['imei'])
                            driver = vehicle.driver.first()

                            t1 = datetime.strptime(str(imei_data['started_at']), "%y-%m-%dT%H:%M:%S")
                            print("\n--------***********----------\n")
                            print(created_at.tzinfo)
                            print("\n--------***********----------\n")

                            t1 = t1.replace(tzinfo=pytz.UTC)
                            duration = (created_at - t1).total_seconds()
                            if duration < 0:
                                duration = 0 - duration
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
                                    vehicle=vehicle
                                )
                            print("trip created --> ", trip)
                            r.delete(str(rt['imei']))
                        except Vehicle.DoesNotExist:
                            r.delete(str(rt['imei']))
                else:
                    if status and not imei_data:
                        print("setting data ..")
                        # set imei data in redis
                        data = {
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
            now = datetime.now()
            print("now is ", now)
            now_minus_1 = now - timedelta(minutes = 10)
            print("noe-10 ", now_minus_1)
            rtd = RealTimeDatabase.objects.filter(created_at__gte=now_minus_1).values(
                "id",
                "imei",
                "ignition_status",
                "latitude",
                "longitude",
                "speed",
                "is_corrupt"
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
                
                if imei_data and len(imei_data)>0:
                    if not status:
                        print(",arking trip as complete")
                        # mark trip as end and store this trip and remove this key from redis
                        start_pos = (imei_data['latitude'], imei_data['longitude'])
                        end_pos = (latitude, longitude)
                        vehicle = Vehicle.objects.get(device__imei_number=rt['imei'])
                        driver = vehicle.driver

                        t1 = datetime.strptime(str(imei_data['started_at']), "%y-%m-%dT%H:%M:%S")
                        duration = (created_at - t1).total_seconds()
                        trip = Trips.objects.create(
                                start_latitude=str(imei_data['latitude']),
                                start_longitude=str(imei_data['longitude']),
                                end_latitude=latitude,
                                end_longitude=longitude,
                                started_at=str(imei_data['started_at']),
                                ended_at=created_at,
                                distance=geodesic(start_pos, end_pos).km,
                                duration=duration,
                                driver=driver,
                                vehicle=vehicle
                            )
                        print("trip created --> ", trip)
                        r.delete(str(rt['imei']))
                else:
                    if status and not imei_data:
                        # set imei data in redis
                        data = {
                            "latitude": latitude,
                            "longitude": longitude,
                            "started_at": datetime.strftime(created_at, "%y-%m-%dT%H:%M:%S")
                        }
                        r.hmset(str(rt['imei']), data)
                # print("imei_data ", imei_data)
                new_id = rt['id']
            if new_id:
                r.set("realtime_last_stored_point", new_id)
            