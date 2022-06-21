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

from sql_app import models, schemas, crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine


# https://api.usgbc.org/arc/data/dev/auth/oauth2/authorize/?subscription-key=5f3f67ada316489e819dca0456904ce8&client_id=ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB&redirect_uri=https://abacuslive.ca&state=a8d5051d-25e9-4c1e-a4e7-d999f9cf0591

# https://abacuslive.ca/?code=Sog6a5XE5DAfn7COn7qc7YuetEktIB&state=a8d5051d-25e9-4c1e-a4e7-d999f9cf0591

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

    print(f"\nstart_date before timezone change: {start_date}")

    # change input datetime to required timezone format
    start_date = change_timezone(start_date, zone)


    print(f"start_date after timezone change: {start_date}")

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

    # append the modified start and end date
    # to a list so as to return
    dates.append(start_date)
    dates.append(end_date)
    print(f"Dates after all processing: {dates}\n")

    return dates


# Function for processing arc data
# Recieve data from send arc consumption frunction
# Based on electrical hierarchy sorts data and adds electrical energy
# Process dates to be send to Arc
# Changes unit of the energy
# Arguments:
# datain: collection of dictionaries coming from panoramic power
# electrical_hierarchy: list of elaments that we have to count when we add energy
# time data: informations about the sites such as duration timezone etc
def process_arc_data(measurements: dict, electrical_hierarchy: list, time_data: dict):

    # initialisation of values
    total_energy = 0.0
    time_data["duration"] = int(time_data["duration"])

    # dictionary to send values to Arc
    arc_dict = measurements[0]


    # loop through different dictionaries in the input
    for measurement in measurements:

        # loop through the electrical hierarchy for calculating energy
        # --> if device name is equal to the electrical hierarchy added
        # Then add the energy to total energy
        for val in electrical_hierarchy:
            if(measurement["device_name"] == val):
                energy = measurement["energy"]
                total_energy = total_energy + energy
                total_energy = round(total_energy, 2)
                print(f"{measurement['device_name']}\tsensor value: {measurement['energy']}\tsum of sensors: {total_energy}")

    # Send measured time to processing time
    # changing time zone
    # changing format
    date_change = start_end_time(arc_dict["measurement_time"], time_data["duartion_format"], time_data["duration"], time_data["time_zone"])

    # Since the measured time has been modified to
    # start date and end date we don't
    # need measurement time field anymore
    del arc_dict["measurement_time"]

    # Data to be send to Arc is added to arc_dict
    # ie. start_date, end_date, total energy
    arc_dict["start_date"] = date_change[0]
    arc_dict["end_date"] = date_change[1]
    arc_dict["energy"] = total_energy/1000

    return arc_dict


# Recieve data for Arc from front end
# Send it for processing
# Send processed data to Arc API function
# Arguments:
# datain: collection of dictionaries coming from panoramic power
# electrical_hierarchy: list of elaments that we have to count when we add energy
# time data: informations about the sites such as duration timezone etc
def send_arc_consumption(db: Session, datain: dict, electrical_hierarchy: str, time_data: dict):

    primary_key = settings.arc_primary_key

    # data in has an inside dictionary with name measurements
    measurements = datain["measurements"]

    # Electrical hierarchy seperate the strings
    electrical_hierarchy = electrical_hierarchy.split(", ")

    # Sending data for processing
    consumption = process_arc_data(measurements, electrical_hierarchy, time_data)
    print(consumption)

    # Sending data to arc
    # --------------------------------un comment -----------------------------
    # create_meter_consumption(db, consumption["leed_id"], consumption["client"], consumption["meter_id"], consumption["start_date"], consumption["end_date"], consumption["energy"])




# Function for processing arc data
# Recieve data from send arc consumption frunction
# Based on electrical hierarchy sorts data and adds Co2
# Process dates to be send to Arc
# Arguments:
# datain: collection of dictionaries coming from panoramic power
# electrical_hierarchy: list of elaments that we have to count when we add energy
# time data: informations about the sites such as duration timezone etc
def process_co2_consumption(measurements: dict, electrical_hierarchy: list, time_data: dict):

    # initialisation of values
    co2 = 0.0
    time_data["duration"] = int(time_data["duration"])

    # dictionary to send values to Arc
    arc_dict = measurements[0]


    # loop through different dictionaries in the input
    for measurement in measurements:

        # loop through the electrical hierarchy for calculating sum of co2
        # --> if device name is equal to the electrical hierarchy in the database
        # Then add the add the co2
        for val in electrical_hierarchy:
            if (measurement["flow"] is not None) and (measurement["meter_name"] == val):
                co2 = co2 + measurement["flow"]
                co2 = round(co2, 2)
                print(f"{measurement['meter_name']}\tsensor value: {measurement['flow']}\tsum of sensors: {co2}")



    # Send measured time to processing time
    # changing time zone
    # changing format
    date_change = start_end_time(arc_dict["measurement_time"], time_data["duartion_format"], time_data["duration"], time_data["time_zone"])

    # Since the measured time has been modified to
    # start date and end date we don't
    # need measurement time field anymore
    del arc_dict["measurement_time"]

    # Data to be send to Arc is added to arc_dict
    # ie. start_date, end_date, total energy
    arc_dict["start_date"] = date_change[0]
    arc_dict["end_date"] = date_change[1]
    arc_dict["flow"] = co2/24

    return arc_dict


# Function for processing arc data
# Recieve data from send arc consumption frunction
# Based on electrical hierarchy sorts data and adds gas consumption
# Process dates to be send to Arc
# Arguments:
# datain: collection of dictionaries coming from panoramic power
# electrical_hierarchy: list of elaments that we have to count when we add energy
# time data: informations about the sites such as duration timezone etc
def process_gas_consumption(measurements: dict, electrical_hierarchy: list, time_data: dict):
   
    # initialisation of values
    gas = 0.0
    time_data["duration"] = int(time_data["duration"])

    # dictionary to send values to Arc
    arc_dict = measurements[0]


    # loop through different dictionaries in the input
    for measurement in measurements:

        # loop through the electrical hierarchy for specific gas meter sensors
        # setup as electrical hierarchy in database
        # --> if device name is equal to the electrical hierarchy in the database
        # Then add the gas sensor value to the sum
        for val in electrical_hierarchy:
            if (measurement["energy"] is not None) and (measurement["meter_name"] == val):
                gas = gas + measurement["energy"]
                gas = round(gas, 2)
                print(f"{measurement['meter_name']}\tsensor value: {measurement['energy']}\tsum of sensors: {gas}")



    # Send measured time to processing time
    # changing time zone
    # changing format
    date_change = start_end_time(arc_dict["measurement_time"], time_data["duartion_format"], time_data["duration"], time_data["time_zone"])

    # Since the measured time has been modified to
    # start date and end date we don't
    # need measurement time field anymore
    del arc_dict["measurement_time"]

    # Data to be send to Arc is added to arc_dict
    # ie. start_date, end_date, total energy
    arc_dict["start_date"] = date_change[0]
    arc_dict["end_date"] = date_change[1]
    arc_dict["meter_name"] = "gas meter"
    arc_dict["energy"] = gas/1000

    return arc_dict



# Recieve data for Arc from front end
# Send it for processing
# Send processed data to Arc API function
# Arguments:
# datain: collection of dictionaries coming from panoramic power
# electrical_hierarchy: list of elaments that we have to count when we add energy
# time data: informations about the sites such as duration timezone etc
def send_arc_co2_consumption(db: Session, datain: dict, electrical_hierarchy: str, time_data: dict):

    primary_key = settings.arc_primary_key

    # co2 = 0
    # arc_time_data = []

    # data in has an inside dictionary with name measurements
    measurements = datain["measurements"]
    # print(measurements)

    # Electrical hierarchy seperate the strings
    electrical_hierarchy = electrical_hierarchy.split(", ")

    # Sending data for processing
    consumption = process_co2_consumption(measurements, electrical_hierarchy, time_data)
    print(consumption)


    # Sending data to arc
    # --------------------------------Uncomment----------------------------
    # create_co2_consumption(db, consumption["leed_id"], consumption["client"], consumption["meter_id"], consumption["start_date"], consumption["end_date"], consumption["energy"])


# Recieve data for Arc from front end
# Send it for processing
# Send processed data to Arc API function
# Arguments:
# datain: collection of dictionaries coming from panoramic power
# electrical_hierarchy: list of elaments that we have to count when we add energy
# time data: informations about the sites such as duration timezone etc
def send_arc_gas_consumption(db: Session, datain: dict, electrical_hierarchy: str, time_data: dict):

    primary_key = settings.arc_primary_key


    # data in has an inside dictionary with name measurements
    measurements = datain["measurements"]
    # print(measurements)

    # Electrical hierarchy seperate the strings
    electrical_hierarchy = electrical_hierarchy.split(", ")
    print(electrical_hierarchy)

    # Sending data for processing
    consumption = process_gas_consumption(measurements, electrical_hierarchy, time_data)
    print(consumption)


    # Sending data to arc
    # --------------------------------Uncomment----------------------------
    # create_gas_consumption(db, consumption["leed_id"], consumption["client"], consumption["meter_id"], consumption["start_date"], consumption["end_date"], consumption["power"])




# creating a meter object in Arc
# Arguments: leed_id - leed id of the given project
# meter_type : meter type 46 for electrical meters
# unit: specifying which unit the data of this meter will have
# meter_id: check meter list API for get meter_id
# name: end point for creating meter ie electricty/water/co2 etc
def create_meter_object(db: Session, leed_id: str, client_name: str, meter_type: int, unit: str, meter_id: str, name: str = "electricity", partner_details: str = "3"):

    primary_key = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, client_name=client_name)

    # headers, params, body and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': primary_key}
    body = {"name": name, "type": meter_type, "native_unit": unit, "partner_details": partner_details, "partner_meter_id": meter_id}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/meters/"

    # convertin body to Json
    json_body = json.dumps(body)
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(f"requests data = {data}")
        # return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Create consumption for meter
# Arguments:
# leed_id: leed_id of the purticular project
# meter_id: id of the purticular meter to which we are entering data
# start_date, end_date: start and ending time and date of the data we are entering
# reading: meter reading for the purticular meter at this given time
def create_meter_consumption(db: Session, leed_id: str, client_name: str, meter_id: str, start_date: str, end_date: str, reading: float):

    primary_key: str = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, client_name=client_name)

    # headers, params, body and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': primary_key}
    body = {"start_date": start_date, "end_date": end_date, "reading": reading}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"

    # converting body of the API to Json
    json_body = json.dumps(body)
   
    # API request
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("meter consumption API error")



# Create consumption for CO2 meter
# Arguments:
# leed_id: leed_id of the purticular project
# meter_id: id of the purticular meter to which we are entering data
# start_date, end_date: start and ending time and date of the data we are entering
# reading: meter reading for the purticular meter at this given time
def create_co2_consumption(db: Session, leed_id: str, client_name: str, meter_id: str, start_date: str, end_date: str, reading: float):

    primary_key: str = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, client_name=client_name)

    # headers, params, body and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': primary_key}
    body = {"start_date": start_date, "end_date": end_date, "reading": reading}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"

    # converting body of the API to Json
    json_body = json.dumps(body)

    # API request
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("meter consumption API error")


# Create consumption for gas/btu meter
# Arguments:
# leed_id: leed_id of the purticular project
# meter_id: id of the purticular meter to which we are entering data
# start_date, end_date: start and ending time and date of the data we are entering
# reading: meter reading for the purticular meter at this given time
def create_gas_consumption(db: Session, leed_id: str, client_name: str, meter_id: str, start_date: str, end_date: str, reading: float):

    primary_key: str = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, client_name=client_name)

    # headers, params, body and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': primary_key}
    body = {"start_date": start_date, "end_date": end_date, "reading": reading}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"

    # converting body of the API to Json
    json_body = json.dumps(body)

    # API request
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("meter consumption API error")
