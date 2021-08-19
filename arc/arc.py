
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
from config import settings
import json
from time import time, ctime
from hashlib import sha256

# ARC_PRIMARY_KEY = "5f3f67ada316489e819dca0456904ce8"
# ARC_SECONDARY_KEY = "119d57b07f75450683186e57a9ffe4f1"

# ARC_CLIENT_ID = "ivh2tLYURNgTwCdcqX2nbl1U5rs2KnHTIAkyXVFB"
# ARC_SECRET = "ujeUGNMu4vPOfjXnWdVDs08Sx9WRQQirr9DXUUOJKq3H5O9eWpJPLPUxzFIxqppWJ9L2MziF2zs02vxMcTLwTsdtvsnXX7LkkAeDpkA5B90FrcFE13Tv3w7jtCUtqhpk"


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
# Arguments
# primary_key - leed primary key of this purticular project
def get_access_token(primary_key: str = settings.arc_primary_key):

    # opening json file to access refresh token
    try:
        with open("first.json", "r") as readfile:
            token = json.load(readfile)
    except FileNotFoundError as e:
        print(f"Error: {FileNotFoundError} Unable to open first.json, in get access token")
        return 101

    # taking the old time added in the Json file when we generated-
    # - the access token last time
    old_time = float(token["current_time"])

    # Check whether the access token has expired
    # access token expires in 10 hours
    access_expired = check_access_expiry(old_time)

    # If "access_expired" is 1: access token expired
    # generate access_token
    if access_expired == 1:
        access_token = generate_auth2_token(primary_key)
        return access_token

    # If "access_expired" is 1: access token expired
    # generate access_token
    else:
        access_token = token["access_token"]
        return access_token


# Function to generate a random string
# generated random string can be used as STATE
# Arguments
# primary_key - leed primary key of this purticular project
def generate_salt(primary_key: str = settings.arc_primary_key):

    # Headers and url for the API request
    headers = {'Ocp-Apim-Subscription-Key': primary_key}
    url = "https://api.usgbc.org/arc/data/dev/auth/oauth2/salt/"

    # API request
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data
    except Exception as error:
        print(f"Error in salt generation: {error}")
        return 101


# generate hash256
def generate_hash(state: str):
    client_id = settings.arc_client_id
    client_secret = settings.arc_secret
    con_string = client_id + client_secret + state
    en_con_string = con_string.encode()
    hashed_str_con = sha256(en_con_string).hexdigest()
    return hashed_str_con


# generate auth2 token for API subscriptions
def generate_auth2_token(primary_key: str = settings.arc_primary_key):

    # opening json file to access refresh token
    try:
        with open("first.json", 'r') as infile:
            token = json.load(infile)
        code = token["refresh_token"]
    except FileNotFoundError as e:
        print("Error: {e} opening first.json in generate_auth2_token")
        return 102

    # generating salt
    salt = generate_salt(primary_key)
    if(salt == 1):
        print("no salt")
        return 103
    state = salt["state"]

    client_secret = generate_hash(state)
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': settings.arc_primary_key}
    body = {"grant_type": "refresh_token", "code": code, "client_id": settings.arc_client_id, "client_secret": client_secret, "state": state}
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



# if __name__ == "__main__":

#     get_access_token()
