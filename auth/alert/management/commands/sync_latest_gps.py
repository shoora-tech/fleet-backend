from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll
from alert.models import RealTimeDatabase, LatestGPS
from organization.models import Organization
from device.models import Device
import boto3
from environ import Env
from django.conf import settings
import json


class Command(BaseCommand):
    help = 'Sync Realtime Data in LatetGps table'

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
        orgs = Organization.objects.all()
        current = list(LatestGPS.objects.all().values_list("imei", flat=True))
        devices = list(Device.objects.all().exclude(imei_number__in=current).values_list("imei_number", flat=True))
        lts = []
        for dev in devices:
            # fetch latest data for this device
            rt = RealTimeDatabase.objects.filter(imei=dev, is_corrupt=False).last()
            if rt:
                print("working for ", dev)
                lt = LatestGPS(
                    location_packet_type=rt.location_packet_type,
                    message_body_length=rt.message_body_length,
                    imei=rt.imei,
                    message_serial_number=rt.message_serial_number,
                    alarm_series=rt.alarm_series,
                    terminal_status=rt.terminal_status,
                    ignition_status=rt.ignition_status,
                    latitude=rt.latitude,
                    longitude=rt.longitude,
                    height=rt.height,
                    speed=rt.speed,
                    direction=rt.direction,
                    is_corrupt=rt.is_corrupt,
                    raw_hex_data=rt.raw_hex_data,
                    device_time=rt.device_time,
                    organization=rt.organization,
                    # created_at=rt["created_at"],
                    # updated_at=rt["updated_at"]
                )
                lts.append(lt)
        LatestGPS.objects.bulk_create(lts, ignore_conflicts=True)
        # for org in orgs:


            