#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
from arc.arc import get_access_token
from config import settings

# ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
# ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

# ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
# ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"

# To get Meter's List and details
# arguments:
# leed_id: leed id of the purticular project
# primary_key: primary key purticular client
def get_meter_list(leed_id: str = "8000037879", primary_key: str = settings.arc_primary_key):

    # header needs access token, so we generate access token
    access_token = get_access_token(primary_key)

    # header and url for accessing the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/"

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
def get_asset_aggregated_data(data_endpoint: str = "electricity", leed_id: str = "8000037879", start_date: str = "2017-10-07", end_date: str = "2017-10-08", unit: str = "kWh", primary_key: str = settings.arc_primary_key):

    # header, url, input params
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    params = urllib.parse.urlencode({'start_date': start_date, 'end_date': end_date, 'unit': unit, 'leed_ids': leed_id})
    url = f"https://api.usgbc.org/arc/data/dev/assets/{data_endpoint}/analytics/?unit={unit}&leed_ids={leed_id}"

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
def get_asset_comprehensive_score(primary_key: str = settings.arc_primary_key, leed_id: str = "8000037879", date: str = "2021-08-11"):

    #url and headers for the API
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/scores/re-entry/?at={date}"

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
def get_asset_score(primary_key: str = settings.arc_primary_key, leed_id: str = "8000037879", date: str = "2021-08-11"):

    # headers, params and url for the API
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    params = urllib.parse.urlencode({'at': date})
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/scores/"

    # API request
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset score API")
        return 105



# function to search for a purticular asset
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
def asset_search(primary_key: str = settings.arc_primary_key, leed_id: str = "8000037879"):

    # To use this API we need access token
    access_token = get_access_token(primary_key)

    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    params = urllib.parse.urlencode({'q': leed_id})
    url = "https://api.usgbc.org/arc/data/dev/assets/search/"

    # API request
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access asset search API")
        return 105



# Function to get asset list
# arguments:
# primary_key - primary key of the client
def get_asset_list(primary_key: str = settings.arc_primary_key):

    # To use this API we need access token
    access_token = get_access_token(primary_key)
   
    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = "https://api.usgbc.org/arc/data/dev/assets/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset list API")
        return 105



# function to get asset object detail
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
def get_asset_object_detail(primary_key: str = settings.arc_primary_key, leed_id: str = "8000037879"):

    # To use this API we need access token
    access_token = get_access_token(primary_key)
   
    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get asset object detail API")
        return 105



# function to get fuel category
# arguments:
# primary_key - primary key of the client
def get_fuel_category(primary_key: str = settings.arc_primary_key):

    # To use this API we need access token
    access_token = get_access_token(primary_key)

    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = "https://api.usgbc.org/arc/data/dev/fuel/category/"
   
    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get fuel category API")
        return 105

# get meter's consumption list
def get_meter_consumption_list(primary_key: str = settings.arc_primary_key, leed_id: str = "8000037879", meter_id: str = "11879657"):

    # To use this API we need access token
    access_token = get_access_token(primary_key)

    # headers, params and url for the API
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"


    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get meter consumption list API")
        return 105


# meter's data consumption object detail
# arguments:
# primary_key - primary key of the client
# leed_id - leed id of the given project
# meter_id - you get meter_id either from Arc
def get_meter_consumption_detail(primary_key: str = settings.arc_primary_key, leed_id: str = "8000037879", meter_id: str = "11586622", meter_number: str = "157798271"):

    # This API requires access token for retrieving data
    access_token = get_access_token(primary_key)

    # Headers and url for the API request
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': primary_key}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/ID:{meter_number}/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e} \n Unable to access get meter consumption API")
        return 105



# if __name__ == "__main__":

    # generate_auth2_code()
    # auth2()
    # generate_hash()
    # generate_auth2_token()
    # create_meter_object()
    # generate_auth2_refresh_token()
    # get_meter_list()
    # get_asset_aggregated_data()
    # get_asset_comprehensive_score()
    # get_asset_score()
    # asset_search()
    # get_asset_list()
    # get_asset_object_detail()
    # get_fuel_category()
    # get_meter_consumption_list()
    # get_meter_consumption_detail()
    # get_current_time()
    # create_meter_consumption()
    # get_access_token()
