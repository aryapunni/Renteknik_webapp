#!/usr/bin/env python3
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json
from hashlib import sha256
from time import time, ctime
# from config import settings

ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"


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
        print(data)
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
        print(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


#

if __name__ == "__main__":

    # generate_auth2_code()
    # auth2()
    # generate_hash()
    # generate_auth2_token()
    # create_meter_object()
    # generate_auth2_refresh_token()
    # get_meter_list()
    # get_current_time()
    create_meter_consumption()
    # get_access_token()
