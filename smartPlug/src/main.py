import base64
import logging
import os
import json
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import os, time
from influxdb_client_3 import InfluxDBClient3, Point
from google.cloud import secretmanager

#Configurations
DEVICE_ID = "ebe42a57503d85c24bzbfd"
DEVICE_MODEL = "SmartPlug"
#list of codes to skip
skipp_list = ["sensor_list", "countdown_1", "cycle_time", "random_time"]

# Get environment variables
SECRETS = None

def load_secrets():
    global SECRETS
    try:
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the secret version.
        name = f"{os.getenv('SECRET_ID')}/versions/latest"
        # Access the secret version.
        response = client.access_secret_version(request={"name": name})
        # Return the decoded payload of the secret.
        SECRETS = json.loads(response.payload.data.decode("UTF-8"))
    except Exception as e:
        print("Error loading secrets: ", e)
        return False
    
    return True



def pull_data(event, context):
    if 'data' not in event:
        print('Error: Invalid Pub/Sub message format')
        return

    if 'data' in event:
        try:
            pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        except Exception as e:
            print('Error: Failed to decode Pub/Sub message:', e)
            return

        print(f"Received Pub/Sub message: {pubsub_message}")
    
        if not load_secrets():
            print("Failed to load secrets.")
            return

        # Enable debug log
        if SECRETS['DEBUG']:
            TUYA_LOGGER.setLevel(logging.DEBUG)


        try:
            # Init OpenAPI and connect
            openapi = TuyaOpenAPI(SECRETS['API_ENDPOINT'], SECRETS['ACCESS_ID'], SECRETS['ACCESS_KEY'])
            openapi.connect()
        except Exception as e:
            print('Error: Failed to connect to Tuya API:', e)
            return

        try:
            client = InfluxDBClient3(host=SECRETS['INFLUXDB_HOST'], token=SECRETS['INFLUXDB_TOKEN'], org=SECRETS['INFLUXDB_ORG'], database=SECRETS['INFLUXDB_DATABASE'])
        except Exception as e:
            print('Error: Failed to connect to InfluxDB or switch database:', e)
            return


        # Get detailed device information
        response = openapi.get("/v2.0/cloud/thing/{}/shadow/properties".format(DEVICE_ID))

        # Check if 'result' and 'properties' keys exist in the response
        if 'result' not in response or 'properties' not in response['result']:
            print('Error: Invalid response format from Tuya API')
            return

        # Process data
        try:
            for item in response["result"]["properties"]:

                # Check if required keys exist in the item
                if not all(key in item for key in ['code', 'dp_id', 'custom_name', 'value']):
                    print('Error: Invalid item format')
                    continue

                # Skip list - this is a list of data that we don't want to write to InfluxDB
                if item["code"] in skipp_list:
                    continue
                
                point = Point(item["code"]).tag("model", DEVICE_MODEL).tag("dp_id", item["dp_id"]).tag("custom_name", item["custom_name"]).field("value", item["value"])
                client.write(point)

        
            #client.write_points(data_points)
            #client.write(bucket=SECRETS['INFLUXDB_BUCKET'], record=data_points)
        except Exception as e:
            print('Error: Failed to write points to InfluxDB:', e)
            return
        finally:
            client.close()
        
        print("Data write complete.")
        
    else:
        print('Error: Invalid Pub/Sub message format')

