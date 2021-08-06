#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
from arc.arc import get_access_token
# from config import settings

ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"

# Get meter's list
# To get Meter's List and details
def get_meter_list(leed_id: str = "8000037879"):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# get aggregated data
# input date and leed id
def get_asset_aggregated_data(data_endpoint: str = "electricity", leed_id: str = "8000037879", start_date: str = "2017-10-07", end_date: str = "2017-10-08", unit: str = "kWh"):
    headers = {'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}

    params = urllib.parse.urlencode({'start_date': start_date, 'end_date': end_date, 'unit': unit, 'leed_ids': leed_id})
    url = f"https://api.usgbc.org/arc/data/dev/assets/{data_endpoint}/analytics/?unit=kwh&leed_ids=8000037879"

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# asset comprehensive score
def get_asset_comprehensive_score():
    access_token = get_access_token()
    headers = {'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    params = urllib.parse.urlencode({})
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/scores/re-entry/"
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# get asset performance/score for a period of time
def get_asset_score():
    headers = {'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    params = urllib.parse.urlencode({})
    url = "https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/scores/"
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        print(data)
        conn = http.client.HTTPSConnection('api.usgbc.org')
        conn.request("GET", "/arc/data/dev/assets/LEED:8000037879/scores/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# function to search for a purticular asset
def asset_search():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    params = urllib.parse.urlencode({'q': '8000037879'})
    url = "https://api.usgbc.org/arc/data/dev/assets/search/"
    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# Function to get asset list
def get_asset_list():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = "https://api.usgbc.org/arc/data/dev/assets/"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# function to get asset object detail
def get_asset_object_detail():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = "https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# function to get fuel category
def get_fuel_category():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = "https://api.usgbc.org/arc/data/dev/fuel/category/"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# get meter's consumption list
def get_meter_consumption_list():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = "https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# meter's data consumption object detail
def get_meter_consumption_detail():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = "https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:157798271/"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(data)
        return data
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
