#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
import pytz
from pytz import timezone, UTC
from datetime import datetime, tzinfo
import time
from time import gmtime, strftime
# from config import settings

ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"


# Time zone conversion
# date: datetime, conversion: str
def find_time_zone():
    datetime_string = "2021-01-01T00:00:00Z"
    start_date = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    est_date = start_date.replace(tzinfo=UTC)
    timezonelist = ['Australia/Adelaide', 'US/Pacific', 'Europe/Berlin', 'Europe/Amsterdam']
    for zone in timezonelist:

        now_time = start_date.now(timezone(zone))
        # print(f"now time = {now_time}")
        est_date = start_date.replace(tzinfo=UTC)
        localtimezone = timezone(zone)
        localDatetime = start_date.astimezone(timezone(zone))
        # print(f"{zone}, \t {start_date}, \t {localDatetime}")
        now = datetime.now()
        # ------- trial two --------- #
        localmoment = localtimezone.localize(start_date, is_dst=None)

        # print(f"{zone}, \t {start_date}, \t {localmoment}")
        utcmoment = localmoment.astimezone(UTC)
        zone = timezone(zone)

        # ------- trial three --------- #

        #---------------------Right method-----------------------------#
        print(f"{start_date}, ---- {pytz.utc.localize(start_date, is_dst=True).astimezone(zone).dst()}")
        print(f"{start_date}, ---- {pytz.utc.localize(start_date, is_dst=None).astimezone(zone)}")
        #---------------------Right method-----------------------------#


def change_timezone(date: datetime, zonename: str):

    print("<------------------------------------------ ********* ------------------------------------------>")
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    input_zone = timezone('UTC')
    zone = timezone(zonename)
    input_datetime = input_zone.localize(date, is_dst=True)
    changed_datetime = zone.localize(date, is_dst=True)
    changed_datetime = input_datetime.astimezone(zone)
    dst = changed_datetime.tzinfo.dst(changed_datetime)
    print(f"zone ---> {zonename}")
    print(f"input ---> {input_datetime}\noutput ---> {changed_datetime}\ndstt ---> {dst}\nreturn value ---> {changed_datetime.strftime(fmt)}")
    print("<------------------------------------------ ********* ------------------------------------------>")



# url for application registration
# https://api.usgbc.org/arc/data/dev/auth/oauth/login/?subscription-key=5f3f67ada316489e819dca0456904ce8
# https://api.usgbc.org/arc/data/dev/auth/oauth2/authorize/?subscription-key=5f3f67ada316489e819dca0456904ce8&client_id=ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB&redirect_uri=https://abacuslive.ca&state=cb16d9ef-4b59-4d43-bd9a-dc503e09447a
# # {
#     "expires_in": 36000,
#     "token_type": "Bearer",
#     "scope": "read write groups",
#     "refresh_token": "KMmqwlEYKHoOD9FQS3nG9h6hlAY80a",
#     "access_token": "nZcRokj2PaovBAU3Rlq6QAThDru5Lz",
#     "state": "cb16d9ef-4b59-4d43-bd9a-dc503e09447a"
# }
# https://abacuslive.ca/?code=eusL1QBBf7aafSm7gJhwpO4soyxaHK&state=0e5fbb92-3afb-4adb-a175-486bdd9c9160


# Function for finding current time
# Linux time
def get_current_time():
    Current_DateTime = time()
    # print(Current_DateTime)
    return Current_DateTime


# Function to check expiry of access token
def check_access_expiry(old_time: float):
    current_time = get_current_time()
    time_difference = current_time - old_time
    if time_difference >= 36000:
        return 1
    else:
        return 0

# function to decide whether accecc token expired
# function returns 0 - Token haven't expired
# Function returns 1 - If token have alreadyexpired
def get_access_token():
    with open("first.json", "r") as readfile:
        token = json.load(readfile)
    old_time = float(token["current_time"])
    access_expired = check_access_expiry(old_time)
    if access_expired == 1:
        access_token = generate_auth2_token()
        return access_token
    else:
        access_token = token["access_token"]
        return access_token

   
# Function to generate a random string
# generated random string can be used as STATE
def generate_salt():
    headers = {'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY,}
    try:
        url = "https://api.usgbc.org/arc/data/dev/auth/oauth2/salt/"
        headers = {'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY,}
        r = requests.get(url, headers=headers)
        data = r.json()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data


# generate hash256
def generate_hash(state: str):
    client_id = ARC_CLIENT_ID
    client_secret = ARC_SECRET
    con_string = client_id + client_secret + state
    en_con_string = con_string.encode()
    hashed_str_con = sha256(en_con_string).hexdigest()
    return hashed_str_con



# generate auth2 token for API subscriptions
def generate_auth2_token():
    with open("first.json", 'r') as infile:
        token = json.load(infile)
    code = token["refresh_token"]
    salt = generate_salt()
    state = salt["state"]
    client_secret = generate_hash(state)
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    body = {"grant_type": "refresh_token", "code": code, "client_id": ARC_CLIENT_ID, "client_secret": client_secret, "state": state}
    json_body = json.dumps(body)
    url = "https://api.usgbc.org/arc/data/dev/auth/oauth2/token/"
    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(f"requests data = {data}")

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    token["refresh_token"] = data["refresh_token"]
    token["access_token"] = data["access_token"]
    current_time = get_current_time()
    token["current_time"] = current_time
    with open("first.json", 'w') as outfile:
        json.dump(token, outfile)
    print(f"token after: {token}\n")
    return token["access_token"]


# creating a meter object in Arc
def create_meter_object(leed_id:str = "8000037879", meter_type:int = 46, unit:str = "kWh", meter_id:str = "44"):
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
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Get meter's list
# To get Meter's List and details
def get_meter_list(leed_id: str = "8000037879"):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        print(json.dumps(data, indent=4, sort_keys=True))
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# meter's data consumption object detail
def get_meter_consumption_detail():
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}

    params = urllib.parse.urlencode({})
    url = "https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:157798271/"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        # print(data)
        print(json.dumps(data, indent=4, sort_keys=True))
        # conn = http.client.HTTPSConnection('api.usgbc.org')
        # conn.request("GET", "/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:157798271/?%s" % params, "{body}", headers)
        # response = conn.getresponse()
        # data = response.read()
        # print(data)
        # conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



# Create consumption for meter
def create_meter_consumption(leed_id: str = "8000037879", meter_id: str = "11586622", start_date: str = "2017-10-06", end_date: str = "2017-10-07", reading: float = 200):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    body = {"start_date": start_date, "end_date": end_date, "reading": reading}
    json_body = json.dumps(body)
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:{leed_id}/meters/ID:{meter_id}/consumption/"

    try:
        r = requests.post(url, headers=headers, data=json_body)
        data = r.json()
        print(json.dumps(data, indent=4, sort_keys=True))

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Arc update function
def update_meter_consumption(start_date: str = "2021-06-21", end_date: str = "2017-06-22", reading: float = 1.38404):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': ARC_PRIMARY_KEY}
    body = {"start_date": start_date, "end_date": end_date, "reading": reading}
    json_body = json.dumps(body)
    params = urllib.parse.urlencode({})
    url = f"https://api.usgbc.org/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:561914/"

    try:
        r = requests.put(url, headers=headers, data=json_body)
        data = r.json()
        print(json.dumps(data, indent=4, sort_keys=True))
        conn = http.client.HTTPSConnection('api.usgbc.org')
        conn.request("PUT", "/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:561914/?%s" % params, f"{json_body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


if __name__ == "__main__":

    # generate_auth2_code()
    # auth2()
    # generate_hash()
    # generate_auth2_token()
    # create_meter_object()
    # generate_auth2_refresh_token()
    datetime_string = "2022-01-01T00:00:00Z"
    start_date = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    # get_meter_list()
    # 'Australia/Adelaide', 'US/Pacific', 'Europe/Berlin' Asia/Jerusalem
    # find_time_zone()
    time_zones = []
    time_zones = pytz.all_timezones
    print(time_zones)
    for zone in time_zones:
        print(zone)
        change_timezone(start_date, zone)
    # get_meter_consumption_detail()
    # update_meter_consumption()
    # get_current_time()
    # create_meter_consumption()
    # get_access_token()
