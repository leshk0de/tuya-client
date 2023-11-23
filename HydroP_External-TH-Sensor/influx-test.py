import os, time
import random
from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv
# Load environment variables from .env file in .venv directory
load_dotenv()

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
host = os.environ.get("INFLUXDB_HOST")

client = InfluxDBClient3(host=host, token=token, org=org, database=os.environ.get("INFLUXDB_DATABASE"))

database="hydrop-testing"

data = {
   "result":{
      "properties":[
         {
            "code":"temp_current",
            "custom_name":"",
            "dp_id":8,
            "time":1699766144779,
            "value":215
         },
         {
            "code":"sensor_list",
            "custom_name":"",
            "dp_id":101,
            "time":1699766144595,
            "value":"AQEBAQEBAA=="
         },
         {
            "code":"ph_current",
            "custom_name":"",
            "dp_id":102,
            "time":1699766144794,
            "value":631
         },
         {
            "code":"ph_warn_max",
            "custom_name":"",
            "dp_id":103,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"ph_warn_min",
            "custom_name":"",
            "dp_id":104,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"temp_warn_max",
            "custom_name":"",
            "dp_id":105,
            "time":1699568898960,
            "value":-100
         },
         {
            "code":"temp_warn_min",
            "custom_name":"",
            "dp_id":106,
            "time":1699568898960,
            "value":-100
         },
         {
            "code":"tds_current",
            "custom_name":"",
            "dp_id":107,
            "time":1699766144887,
            "value":1388
         },
         {
            "code":"tds_warn_max",
            "custom_name":"",
            "dp_id":108,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"tds_warn_min",
            "custom_name":"",
            "dp_id":109,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"ec_current",
            "custom_name":"",
            "dp_id":110,
            "time":1699766144984,
            "value":2770
         },
         {
            "code":"ec_warn_max",
            "custom_name":"",
            "dp_id":111,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"ec_warn_min",
            "custom_name":"",
            "dp_id":112,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"salinity_current",
            "custom_name":"",
            "dp_id":113,
            "time":1699766145160,
            "value":1619
         },
         {
            "code":"salinity_warn_max",
            "custom_name":"",
            "dp_id":114,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"salinity_warn_min",
            "custom_name":"",
            "dp_id":115,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"pro_current",
            "custom_name":"",
            "dp_id":116,
            "time":1699766145249,
            "value":999
         },
         {
            "code":"pro_warn_max",
            "custom_name":"",
            "dp_id":117,
            "time":1699568898960,
            "value":500
         },
         {
            "code":"pro_warn_min",
            "custom_name":"",
            "dp_id":118,
            "time":1699568898960,
            "value":500
         },
         {
            "code":"orp_current",
            "custom_name":"",
            "dp_id":119,
            "time":1699766145337,
            "value":0
         },
         {
            "code":"orp_warn_max",
            "custom_name":"",
            "dp_id":120,
            "time":1699568898960,
            "value":-2000
         },
         {
            "code":"orp_warn_min",
            "custom_name":"",
            "dp_id":121,
            "time":1699568898960,
            "value":-2000
         },
         {
            "code":"cf_current",
            "custom_name":"",
            "dp_id":136,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"cf_warn_max",
            "custom_name":"",
            "dp_id":137,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"cf_warn_min",
            "custom_name":"",
            "dp_id":138,
            "time":1699568898960,
            "value":1
         },
         {
            "code":"rh_current",
            "custom_name":"",
            "dp_id":139,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"rh_warn_max",
            "custom_name":"",
            "dp_id":140,
            "time":1699568898960,
            "value":0
         },
         {
            "code":"rh_warn_min",
            "custom_name":"",
            "dp_id":141,
            "time":1699568898960,
            "value":0
         }
      ]
   },
   "success":True,
   "t":1699766146783,
   "tid":"8943926b811a11ee8365967f1e1b5c8e"
}

DEVICE_ID = "ebe49d5b115ec2631cxghe"
DEVICE_MODEL = "pH-W3988"
skipp_list = ["sensor_list"]

for item in data["result"]["properties"]:
                
  # Check if required keys exist in the item
  if not all(key in item for key in ['code', 'dp_id', 'custom_name', 'value']):
      print('Error: Invalid item format')
      continue

  # Skip list - this is a list of data that we don't want to write to InfluxDB
  if item["code"] in skipp_list:
      continue

  point = Point(item["code"]).tag("model", DEVICE_MODEL).tag("dp_id", item["dp_id"]).tag("custom_name", item["custom_name"]).field("value", item["value"])

  client.write(point)
  print(point)

print("Complete. Return to the InfluxDB UI.")

'''

 point = Point(item["code"]).tag("model": DEVICE_MODEL).tag(
          "dp_id": item["dp_id"]).tag(
          "custom_name": item["custom_name"]
      ).field("value", item["value"])


.tag({
          "model": DEVICE_MODEL,
          "dp_id": item["dp_id"],
          "custom_name": item["custom_name"]
      }
'''