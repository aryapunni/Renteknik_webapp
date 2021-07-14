#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
# from arc_api_test import get_access_token
# from config import settings
from arc.arc import get_access_token
from datetime import datetime, timedelta


ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"



# Function to change the date value to Arc format string
def date_to_string(date: datetime, ):
    date = str(date.date()) + "T" + str(date.time())
    return date


   
# To convert measured time to proper datetime format
def start_end_time(datetime_string, duration_format, duration):
    dates = []
    start_date = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    if duration_format == "minutes":
        end_date = date_to_string(start_date + timedelta(minutes=duration))
        start_date = date_to_string(start_date)
    elif duration_format == "hours":
        end_date = date_to_string(start_date + timedelta(hours=duration))
        start_date = date_to_string(start_date)
    elif duration_format == "days":
        end_date = str(start_date.date() + timedelta(days=duration))
        start_date = str(start_date.date())
    # print("---------------------------------")
    # print(f"start date before 5 minutes {start_date}")
    # print(f"end date after adding 5 minutes {end_date}")
    # print("---------------------------------")
    dates.append(start_date)
    dates.append(end_date)
    return dates


# Function for processing arc data
def process_arc_data(measurements: dict):
    total_energy = 0
    arc_dict = measurements[0]
    for measurement in measurements:
        if((measurement["device_name"] == "RP Sub Main") || (measurement["device_name"] == "LP Sub Main")):
            energy = measurement["energy"]
            total_energy = total_energy + energy
    date_change = start_end_time(arc_dict["measurement_time"], "hours", 1)
    del arc_dict["measurement_time"]
    arc_dict["start_date"] = date_change[0]
    arc_dict["end_date"] = date_change[1]
    arc_dict["energy"] = total_energy/1000
    # print(arc_dict)
    return arc_dict


# Process data from application
def send_arc_consumption(datain: dict):
    measurements = datain["measurements"]
    consumption = process_arc_data(measurements)
    create_meter_consumption(consumption["leed_id"], consumption["meter_id"], consumption["start_date"], consumption["end_date"], consumption["energy"])


# creating a meter object in Arc
def create_meter_object(leed_id:str = "8000037879", meter_type:int = 46, unit:str = "kWh", meter_id:str = "126030"):
    name = "electricity"
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    body = {"name": name, "type": meter_type, "native_unit": unit, "partner_details": "3", "partner_meter_id": meter_id}
    json_body = json.dumps(body)
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/"
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(f"requests data = {data}")
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Create consumption for meter
def create_meter_consumption(leed_id: str, meter_id: str, start_date: str, end_date: str, reading: float):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    body = {"start_date": start_date, "end_date": end_date, "reading": reading}
    json_body = json.dumps(body)
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"
    print(json_body)
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(data)
        # return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# if __name__ == "__main__":

    # generate_auth2_code()
    # auth2()
    # generate_hash()
    # generate_auth2_token()
    # create_meter_object()
    # generate_auth2_refresh_token()
    # get_meter_list()
    # get_current_time()
    # create_meter_consumption()
    # get_access_token()
