import logging
import os
import json
from dotenv import load_dotenv
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import os, time
import random
from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv
# Load environment variables from .env file in .venv directory

# Load environment variables from .env file in .venv directory
load_dotenv()

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
host = os.environ.get("INFLUXDB_HOST")
client = InfluxDBClient3(host=host, token=token, org=org)
database="hydrop-testing"

# Get environment variables
API_ENDPOINT = os.getenv('API_ENDPOINT')
ACCESS_ID = os.getenv('ACCESS_ID')
ACCESS_KEY = os.getenv('ACCESS_KEY')   

# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()


# Set up device_id
DEVICE_ID ="ebe49d5b115ec2631cxghe"



# Call APIs from Tuya
# Get detailed device information
response = openapi.get("/v2.0/cloud/thing/{}/shadow/properties".format(DEVICE_ID))

for point in response["result"]["properties"]:
  
  if point["code"] == "sensor_list":
    continue

  point = (
    Point(point["code"])
    .tag("code", point["code"])
    .field(point["code"], point["value"])
  )
  print("writing point: ", point)
  client.write(database=database, record=point)
  time.sleep(1) # separate points by 1 second
