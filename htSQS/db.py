import mysql.connector
import datetime
import json
import uuid
import string
import secrets
mydb = mysql.connector.connect(host="shoora-mysql.crpd6o4smocv.ap-south-1.rds.amazonaws.com", user="shoora", database="shoora", password="mSpF8KuZ9LsmdjrLC4GQ")
mycursor = mydb.cursor()
# get last saved point

last_save_point_query = """
    SELECT next_query_time
    FROM shoora_pos_query_time
    limit 1;
"""

query_time = mycursor.execute(last_save_point_query)
# if query_time:

myresult = mycursor.fetchall()
next_time = (datetime.datetime.now()-datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
flag = False
for x in myresult:
    flag = True
    print(x[0])
    next_time = x[0].strftime("%Y-%m-%d %H:%M:%S")

print("next time is", next_time)

# update next_time in db


# event_query = """
#     SELECT *
#     FROM tc_events
#     where eventtime >= "%s";
# """ %(next_time)

# mycursor.execute(event_query)
# myresult = mycursor.fetchall()
# # print(myresult[0])
# for x in myresult:
#     print(x)


def format_position_data(result, next_time):
    x = {}
    alphabet = string.ascii_letters + string.digits

    x["specversion"]= "1.0"
    x["id"]= ''.join(secrets.choice(alphabet) for i in range(64))
    x["type"]= "com.aeris.aertrak.trips"
    x["source"]= "/aeris/aertrak"
    x["operation"]= "upsert"
    x["time"]= datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    x["serviceaccount"]= "100040"
    data = []
    for res in result:
        attrs = json.loads(res[5])
        temp = {}
        temp['assetUid'] = '16da58b0-5796-11e9-bd3b-5535c69ce0f8'
        temp['locationTime'] = res[3].strftime('%s')
        temp['heading'] = res[4]
        temp['latitude'] = res[0]
        temp['longitude'] = res[1]
        temp['deviceId'] = res[7]
        temp['speed'] = res[6]
        temp['deviceStatus'] = attrs['motion']
        temp['engineState'] = attrs['ignition']
        temp['accountId'] = '100520'
        temp['deviceBatteryVoltage'] = attrs['battery']
        temp['asset_id'] = '501606'
        temp['eventTime'] = res[2].strftime('%s')
        temp['assetBatteryVoltage'] = attrs['battery']
        data.append(temp)
        next_time = res[2].strftime("%Y-%m-%d %H:%M:%S")
    x['data'] = data
    return next_time, x

query = """
    SELECT 
        tc_positions.latitude,
        tc_positions.longitude,
        tc_positions.servertime,
        tc_positions.devicetime,
        tc_positions.course,
        tc_positions.attributes,
        tc_positions.speed,
        tc_devices.uniqueid
    FROM tc_positions
    INNER JOIN tc_devices on (tc_positions.deviceid = tc_devices.id)
    where servertime >= "%s";
""" %(next_time)

mycursor.execute(query)
myresult = mycursor.fetchall()

next_time, data = format_position_data(myresult, next_time)
print("data is ", json.dumps(data))


# update_nxt_query = """UPDATE shoora_pos_query_time SET next_query_time = "%s" where id = 1; """
# if not flag:
#     update_nxt_query = """INSERT INTO shoora_pos_query_time (next_query_time) values("%s") """%(next_time)

# values = (next_time,)

# print(update_nxt_query)
# mycursor.execute(update_nxt_query)
# mydb.commit()
