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


headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': '{subscription key}'}

params = urllib.parse.urlencode({})

try:
    conn = http.client.HTTPSConnection('api.usgbc.org')
    conn.request("PUT", "/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:157798271/?%s" % params, "{body}", headers)
        # conn.request("GET", "/arc/data/dev/assets/LEED:8000037879/meters/ID:11586622/consumption/ID:157798271/?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
