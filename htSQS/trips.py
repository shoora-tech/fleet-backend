# grab trips 
# fetch events table from last_fetched_time listed in trip_last_fetch_time
# store ignition_on event in local bucket ( redis will be better and preffered )
# for every next iteration if the event is from same device, update the idle time and trip time accordingly

import mysql.connector
import datetime
import json

IGNITION_ON = "ignitionOn"
IGNITION_OFF = "ignitionOff"
DEVICE_MOVING = "deviceMoving"
DEVICE_STOPPED = "deviceStopped"

device_trips_status = {}
trip_cache_template = {
    "device_id": None,
    "status": None,
    "event_time": None,
    "idle_time": 0,
    "trip_time": 0,
    "start_time": None
}

def handle_device_ongoing_trip(device_id, current_event):
    current_trip = device_trips_status.get(str(device_id))
    idle_time = None
    trip_time = None
    if current_trip:
        # an ongoing trip is happening
        previous_event = current_trip['status']
        if current_event['status'] == DEVICE_MOVING:
            # update time by calculating elapsed time between current and previous event
            previous_time = current_trip['event_time']
            # current_time = datetime.datetime.strftime(current_event['event_time'], "%Y-%m-%d %H:%M:%S")
            current_time = current_event['event_time']
            idle_time = (current_time - previous_time).total_seconds()
            trip_time = 0
        if current_event['status'] == IGNITION_OFF:
            # update time by calculating elapsed time between current and previous event
            previous_time = current_trip['event_time']
            # current_time = datetime.datetime.strptime(current_event['event_time'], "%Y-%m-%d %H:%M:%S")
            current_time = current_event['event_time']
            idle_time = (current_time - previous_time).total_seconds()
        
        if current_event['status'] == DEVICE_STOPPED:
            # update time by calculating elapsed time between current and previous event
            start_time = current_trip['start_time']
            # current_time = datetime.datetime.strptime(current_event['event_time'], "%Y-%m-%d %H:%M:%S")
            current_time = current_event['event_time']
            trip_time = (current_time - start_time).total_seconds()
    
    return idle_time, trip_time
        

def calculate_trip_from_events(result):
    trips = []
    for res in result:
        # check if any trip is in progress for this device
        print("res is ", res[1])
        current_event = {}
        trip_cache_template['device_id'] = res[2]
        trip_cache_template['status'] = res[0]
        trip_cache_template['event_time'] = res[1]
        if res[0] == IGNITION_ON:
            # set start time
            trip_cache_template["start_time"] = res[1]
            device_trips_status[str(res[2])] = trip_cache_template
        else:
            idle_time, trip_time = handle_device_ongoing_trip(res[2], trip_cache_template)
            if idle_time:
                trip_cache_template['idle_time'] += idle_time
                device_trips_status[str(res[2])] = trip_cache_template
            if trip_time:
                trip_cache_template['trip_time'] += trip_time
                # remove device id from the bucket as trip ended now
                trip = device_trips_status.pop(res[2])
                trips.append(trip)
    return trips


# Fetch last time data 
mydb = mysql.connector.connect(host="shoora-mysql.crpd6o4smocv.ap-south-1.rds.amazonaws.com", user="shoora", database="shoora", password="mSpF8KuZ9LsmdjrLC4GQ")
mycursor = mydb.cursor()

last_save_point_query = """
    SELECT next_query_time
    FROM shoora_query_time
    limit 1;
"""

query_time = mycursor.execute(last_save_point_query)
# if query_time:

myresult = mycursor.fetchall()
print(myresult)
next_time = (datetime.datetime.now()-datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
flag = False
for x in myresult:
    print("gotch")
    flag = True
    print(x[0])
    next_time = x[0].strftime("%Y-%m-%d %H:%M:%S")

print("next time is", next_time)

until_time =  (datetime.datetime.now()-datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
print("until time is ", until_time)

query = """
    SELECT 
        tc_events.type,
        tc_events.eventtime,
        tc_devices.uniqueid
    FROM tc_events
    INNER JOIN tc_devices on (tc_events.deviceid = tc_devices.id)
    where tc_events.eventtime >= "%s" and tc_events.eventtime <= "%s";
""" %(next_time, until_time)

mycursor.execute(query)
myresult = mycursor.fetchall()

trips = calculate_trip_from_events(myresult)
print("data is ", trips)
mydb.close()

