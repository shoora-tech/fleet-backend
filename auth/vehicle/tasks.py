from celery import shared_task
from vehicle.models import VehicleGeofence, Geofence
from django.core.cache import cache
import redis
from django.conf import settings

# r = redis.Redis(
#     host='redis',
#     port=6379, 
#     db=0,
#     charset="utf-8",
#     decode_responses=True
#     )
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT, 
    db=0,
    charset="utf-8",
    decode_responses=True
    )

@shared_task
def update_geofence_redis(geofence_id, geo_object):
    print("saving obj ... ")
    r.set(geofence_id, geo_object)


@shared_task
def remove_geofence_redis(geofence_id):
    r.delete(geofence_id)

@shared_task
def remove_geofence_from_vehicles_redis(vehicle_geofence_ids):
    for vehicle_geofence_id in vehicle_geofence_ids:
        vg = VehicleGeofence.objects.get(uuid=vehicle_geofence_id)
        # update the redis for each vehicle
        vehicles = list(vg.vehicle.all().values_list("uuid", flat=True))
        vehicles_in_group = list(vg.vehicle_group.all().values_list("vehicle__uuid", flat=True))
        all_vehicles = list(set(vehicles + vehicles_in_group))
        geofence = Geofence.objects.get(uuid=vg.geofence.uuid).values("uuid")
        for vehicle in all_vehicles:
            r.lpop(str(vehicle), str(geofence["uuid"]))


@shared_task
def remove_geofence_from_vehicle_geofence_redis(vehicle_geofence_id):
    vg = VehicleGeofence.objects.get(uuid=vehicle_geofence_id)
    # update the redis for each vehicle
    vehicles = list(vg.vehicle.all().values_list("uuid", flat=True))
    
    vehicles_in_group = list(vg.vehicle_group.all().values_list("vehicle__uuid", flat=True))
    all_vehicles = list(set(vehicles + vehicles_in_group))
    geofence = Geofence.objects.get(uuid=vg.geofence.uuid).values("uuid")
    for vehicle in all_vehicles:
        r.lpop(str(vehicle), str(geofence["uuid"]))
    


@shared_task
def update_vehicle_geofence_redis(vehicle_geofence_id):
    vg = VehicleGeofence.objects.get(uuid=vehicle_geofence_id)
    # update the redis for each vehicle
    vehicles = list(vg.vehicle.all().values_list("device__imei_number", flat=True))
    vehicles_in_group = list(vg.vehicle_group.all().values_list("vehicle__device__imei_number", flat=True))
    all_vehicles = list(set(vehicles + vehicles_in_group))
    geofence = Geofence.objects.get(uuid=vg.geofence.uuid)
    # get all vehicles for thos geofence
    try:
        vehicles = r.lrange(str(geofence.uuid), 0, -1)
        if vehicles:
            for vehicle in vehicles:
                if vehicle not in all_vehicles:
                    key = "geofence_"+str(vehicle)
                    r.lpop(key, str(geofence.uuid))
    except redis.exceptions.ResponseError:
        pass
    for v in all_vehicles:
        key = "geofence_"+str(v)
        r.lpush(key, str(geofence.uuid))

