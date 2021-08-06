#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
# from arc_api_test import get_access_token
from config import settings
from pytz import timezone, UTC
from arc.arc import get_access_token
from datetime import datetime, timedelta, tzinfo


# ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
# ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

# ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
# ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"



# Function to change one time zone to another
# inputs: date to be changed: in date time format
# zone name: The zone to which the given date should be converted
def change_timezone(date: datetime, zonename: str):
    # out put format of changed timezone
    fmt = "%Y-%m-%dT%H:%M:%S"

    # assigning input date as UTC time format
    input_zone = timezone('UTC')

    # change input date to changed time zone
    zone = timezone(zonename)
    input_datetime = input_zone.localize(date, is_dst=True)
    changed_datetime = zone.localize(date, is_dst=True)
    changed_datetime = input_datetime.astimezone(zone)

    # change returning timezone changed date to required format
    changed_datetime = changed_datetime.strftime(fmt)
    return_date = datetime.strptime(changed_datetime, fmt)
    return return_date



# To convert measured time to proper datetime and zone
def start_end_time(datetime_string: str, duration_format: str, duration: int, zone: str):
    # array initialization
    dates = []

    # date time format for sending to Arc
    fmt = "%Y-%m-%dT%H:%M:%S"

    # Removing the extra z from the panpower data
    # Inorder to make the date format compatible with Arc
    if datetime_string.endswith('Z'):
        datetime_string = datetime_string[:-1]

    # change input string to datetime format
    start_date = datetime.strptime(datetime_string, fmt)

    # change input datetime to required timezone format
    start_date = change_timezone(start_date, zone)

    # Three categories of end times:
    # 1. when duration is in minutes --> First condition
    # 2. when duration is in hours   --> Second condition
    # 3. when duration is in days    --> Third condition

    if duration_format == "minutes":
        # add duration to starting datetime
        end_date = start_date + timedelta(minutes=duration)

        # convert both start and end date time to Arc required string format
        end_date = end_date.strftime(fmt)
        start_date = start_date.strftime(fmt)

    elif duration_format == "hours":
        # add duration to starting datetime
        end_date = start_date + timedelta(hours=duration)

        # convert both start and end date time to Arc required string format
        end_date = end_date.strftime(fmt)
        start_date = start_date.strftime(fmt)

    elif duration_format == "days":
        # add duration to starting datetime
        end_date = start_date.date() + timedelta(days=duration)

        # convert both start and end date time to Arc required string format
        end_date = end_date.strftime(fmt)
        start_date = start_date.strftime(fmt)

    dates.append(start_date)
    dates.append(end_date)
    return dates


# Function for processing arc data
def process_arc_data(measurements: dict):
    total_energy = 0
    arc_dict = measurements[0]
    for measurement in measurements:
        if((measurement["device_name"] == "RP Sub Main") | (measurement["device_name"] == "LP Sub Main")):
            energy = measurement["energy"]
            total_energy = total_energy + energy
    date_change = start_end_time(arc_dict["measurement_time"], "hours", 1, 'Canada/Pacific')
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
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': settings.arc_primary_key}
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
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': settings.arc_primary_key}
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
