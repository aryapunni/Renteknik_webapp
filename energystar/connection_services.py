#!/usr/bin/env python3


import requests
from xml.etree import ElementTree
from requests.auth import HTTPBasicAuth


# accept a connection request from a customer
# parameter: customer ID of the purticular customer
def accept_connection_request(accountId: str = "378544"):

    # accept connection url
    url = f"https://portfoliomanager.energystar.gov/wstest/connect/account/{accountId}"

    # header
    headers = {"Content-Type": "application/xml"}


    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <sharingResponse>
    <action>Accept</action>
    <note>Your connection request has been verified and accepted.</note>
    </sharingResponse>'''

    response = requests.post(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# To reject a connection request from a customer
# Parameter: customer ID of the purticular customer
def reject_connection_request(accountId: str = "37854"):

    # accept connection url
    url = f"https://portfoliomanager.energystar.gov/wstest/connect/account/{accountId}"

    # header
    headers = {"Content-Type": "application/xml"}


    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <sharingResponse>
    <action>Reject</action>
    <note>Unfortunately we cannot provide services for you at this time.</note>
    </sharingResponse>'''


    response = requests.post(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# get pending connection requests from customers
def get_pending_connection_requests(pageNumber: str = "0"):

    url = f"https://portfoliomanager.energystar.gov/wstest/connect/account/pending/list?page={pageNumber}"
    response = requests.get(url, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# ----------- ***ALERT*** NOT SURE IF THIS FUNCTION WORKS ---------- #
# To disconnect from a specific customer
# specific customer id as input parameter
# keepshares - whether to keep any meters/data that are already created while deleteing the account(optional)
def disconnect_customer(accountId: str = "37854", keepShares: str = "False"):

    # accept connection url
    url = f"https://portfoliomanager.energystar.gov/wstest/disconnect/account/{accountId}?keepShares={keepShares}"

    # header
    headers = {"Content-Type": "application/xml"}


    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <terminateSharingResponse>
    <note>Account is delinquent.</note>
    </terminateSharingResponse>'''


    response = requests.post(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# get the unread notifications in your account
# parameter: clear - if True (default) clears all the read notification
#                    if False sets all the notifications to unread
def get_notifications(clear: str = "False"):

    url = f"https://portfoliomanager.energystar.gov/wstest/notification/list?clear={clear}"
    response = requests.get(url, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)

# accepts a meter share request from a customer
# parameter: meter ID of the purticular customer
def accept_meter_share_request(meterId: str = "456345"):

    # accept connection url
    url = f"https://portfoliomanager.energystar.gov/wstest/share/meter/{meterId}"

    # header
    headers = {"Content-Type": "application/xml"}


    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <sharingResponse>
    <action>Accept</action>
    <note>Your connection request has been verified and accepted.</note>
    </sharingResponse>'''

    response = requests.post(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# accepts a meter share request from a customer
# parameter: meter ID of the purticular customer
def accept_meter_share_request(meterId: str = "456345"):

    # accept connection url
    url = f"https://portfoliomanager.energystar.gov/wstest/share/meter/{meterId}"

    # header
    headers = {"Content-Type": "application/xml"}


    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <sharingResponse>
    <action>Accept</action>
    <note>Your connection request has been verified and accepted.</note>
    </sharingResponse>'''

    response = requests.post(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)



if __name__ == "__main__":

    print("hello world")
    # accept_connection_request()
    # reject_connection_request()
    # get_pending_connection_requests()
    # disconnect_customer()
    # get_notifications()
    accept_meter_share_request()
