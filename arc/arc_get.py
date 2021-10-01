#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
from arc.arc import get_access_token
from config import settings


from sql_app import models, schemas, crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
from fastapi import Depends


# ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
# ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

# ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
# ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"

# To get Meter's List and details
# arguments:
# leed_id: leed id of the purticular project
# primary_key: primary key purticular client
def get_meter_list(db: Session, leed_id: str, client_name: str):

    primary_key = settings.arc_primary_key

    # header needs access token, so we generate access token

    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)

    # header and url for accessing the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/meters/"

    # API reuest
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get meter list API")
        return 105


# get aggregated data
# Function Arguments:
# data_endpoint - end point for fetching data
# leed_id - leed id of the given project
# start_gate - from which date the data should be fetched
# end_gate - upto which date the data should be fetched
# unit - unit of the data
# primary_key - primary key of the client
def get_asset_aggregated_data(data_endpoint: str, leed_id: str, start_date: str, end_date: str, unit: str):

    primary_key: str = settings.arc_primary_key
   
    # header, url, input params
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    params = urllib.parse.urlencode({'start_date': start_date, 'end_date': end_date, 'unit': unit, 'leed_ids': leed_id})
    url = f"{settings.arc_url}/assets/{data_endpoint}/analytics/?unit={unit}&leed_ids={leed_id}"

    # API request
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to Access get asset aggregated data API")
        return 105


# To get the comprehensive score that Arc assigned to the project
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
# date - Date to which we are requesting the comprehensive score
def get_asset_comprehensive_score(leed_id: str, date: str):

    primary_key: str = settings.arc_primary_key

    #url and headers for the API
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/scores/re-entry/?at={date}"

    #API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset comprehensive score API")
        return 105


# get asset performance/score for a period of time
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
# date - Date to which we are requesting the score
def get_asset_score(leed_id: str, date: str):

    primary_key = settings.arc_primary_key
    # headers, params and url for the API
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    params = urllib.parse.urlencode({'at': date})
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/scores/"

    # API request
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        # print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset score API")
        return 105



# function to search for a purticular asset
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
def asset_search(db: Session, leed_id: str, client_name: str):

    primary_key = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)

    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    params = urllib.parse.urlencode({'q': leed_id})
    url = f"{settings.arc_url}/assets/search/"

    # API request
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        # print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access asset search API")
        return 105



# Function to get asset list
# arguments:
# primary_key - primary key of the client
def get_asset_list(db: Session, leed_id: str, client_name: str):

    primary_key = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)
   
    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/assets/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        # print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset list API")
        return 105



# function to get asset object detail
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
def get_asset_object_detail(db: Session, leed_id: str, client_name: str):

    primary_key = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)
   
    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        # print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset object detail API")
        return 105



# function to get fuel category
# arguments:
# primary_key - primary key of the client
def get_fuel_category(db: Session, leed_id: str, client_name: str):

    primary_key: str = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)

    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/dev/fuel/category/"
   
    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        # print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get fuel category API")
        return 105

# get meter's consumption list
def get_meter_consumption_list(db: Session, leed_id: str, client_name: str, meter_id: str):

    primary_key: str = settings.arc_primary_key

    # To use this API we need access token
    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)

    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/dev/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"


    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get meter consumption list API")

        return 105


# meter's data consumption object detail
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
# meter_id - you get meter_id either from Arc
def get_meter_consumption_detail(db: Session, leed_id: str, meter_id: str, client_name: str):

    primary_key: str = settings.arc_primary_key

    # This API requires access token for retrieving data
    access_token = get_access_token(db=db, leed_id=leed_id, client_name=client_name)

    # Headers and url for the API request
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"{settings.arc_url}/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/" #ID:{meter_number}/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        # print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get meter consumption API")
        return 105


