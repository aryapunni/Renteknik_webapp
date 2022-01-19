#!/usr/bin/env python3

import requests
from xml.etree import ElementTree
from requests.auth import HTTPBasicAuth

# username: Renteknik-Group
# password: Renteknik123
# id: 378524
# new customer -- Renteknik group
# -- id = 378544
# -- get url = /customer/378544

def create_account_test():

    username = "Renteknik-Group"
    #url for creating account
    url = "https://portfoliomanager.energystar.gov/wstest/account"

    headers = {"Content-Type": "application/xml"}

    # body of the request
    body = f'''<?xml version="1.0" encoding="UTF-8"?>
    <account>
    <username>{username}</username>
    <password>Renteknik123</password>
    <webserviceUser>true</webserviceUser>
    <searchable>true</searchable>
    <billboardMetric>score</billboardMetric>
    <contact>
    <firstName>Renteknik</firstName>
    <lastName>Group</lastName>
    <address address1="Harvester Rd" city="Burlington" state="ON" postalCode="L6K3R6" country="CA"/>
    <email>engineering@renteknikgroup.com</email>
    <jobTitle>Energy management consultants</jobTitle>
    <phone>9056343888 </phone>
    </contact>
    <organization name="Renteknik Group Inc.">
    <primaryBusiness>Other</primaryBusiness>
    <otherBusinessDescription>other</otherBusinessDescription>
    <energyStarPartner>true</energyStarPartner>
    <energyStarPartnerType>Service and Product Providers</energyStarPartnerType>
    </organization>
    <emailPreferenceCanadianAccount>true</emailPreferenceCanadianAccount>
    </account>'''

    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?><response status="Ok"><id>378524</id><links><link linkDescription="This is the GET url for this Account." link="/account" httpMethod="GET"/></links></response>
    response = requests.post(url, headers=headers, data=body)
    print(response.content)
    # tree = ElementTree.fromstring(response.content)
    # print(tree())

# get account details
def get_account_details():

    # get account url
    url = "https://portfoliomanager.energystar.gov/wstest/account"

    response = requests.get(url, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# create customer
def create_customer():

    # Customer details
    # All of these parameters should be coming as function arguments
    customer = {"username": "Renteknikgroupoffice",
                "password": "Renteknikgroup123",
                "firstname": "Darren",
                "lastname": "Cooper",
                "address": '"8-5195 Harvester Rd"',
                "city": '"Burlington"',
                "state": '"ON"',
                "postalcode": '"L7L 6E9"',
                "country": '"CA"',
                "email": "d.cooper@renteknikgroup.com",
                "jobTitle": "president",
                "phone": "905-634-3888",
                "organaization": '"Renteknik Group Inc"'}

    # create customer url
    url = "https://portfoliomanager.energystar.gov/wstest/customer"

    # header
    headers = {"Content-Type": "application/xml"}


    if customer["country"] == "CA":

        body = f'''<?xml version="1.0" encoding="UTF-8"?>
        <account>
        <username>{customer["username"]}</username>
        <password>{customer["password"]}</password>
        <webserviceUser>true</webserviceUser>
        <searchable>false</searchable>
        <billboardMetric>score</billboardMetric>
        <contact>
        <firstName>{customer["firstname"]}</firstName>
        <lastName>{customer["lastname"]}</lastName>
        <address address1={customer["address"]} city={customer["city"]} state={customer["state"]} postalCode={customer["postalcode"]} country={customer["country"]}/>
        <email>{customer["email"]}</email>
        <jobTitle>{customer["jobTitle"]}</jobTitle>
        <phone>{customer["phone"]}</phone>
        </contact>
        <organization name={customer["organaization"]}>
        <primaryBusiness>Other</primaryBusiness>
        <otherBusinessDescription>other</otherBusinessDescription>
        <energyStarPartner>true</energyStarPartner>
        <energyStarPartnerType>Service and Product Providers</energyStarPartnerType>
        </organization>
        <emailPreferenceCanadianAccount>true</emailPreferenceCanadianAccount>
        </account>'''

    else:

        body = f'''<?xml version="1.0" encoding="UTF-8"?>
        <account>
        <username>{customer["username"]}</username>
        <password>{customer["password"]}</password>
        <webserviceUser>true</webserviceUser>
        <searchable>false</searchable>
        <billboardMetric>score</billboardMetric>
        <contact>
        <firstName>{customer["firstname"]}</firstName>
        <lastName>{customer["lastname"]}</lastName>
        <address address1={customer["address"]} city={customer["city"]} state={customer["state"]} postalCode={customer["postalcode"]} country={customer["country"]}/>
        <email>{customer["email"]}</email>
        <jobTitle>{customer["jobTitle"]}</jobTitle>
        <phone>{customer["phone"]}</phone>
        </contact>
        <organization name={customer["organaization"]}>
        <primaryBusiness>Other</primaryBusiness>
        <otherBusinessDescription>other</otherBusinessDescription>
        <energyStarPartner>true</energyStarPartner>
        <energyStarPartnerType>Service and Product Providers</energyStarPartnerType>
        </organization>
        </account>'''

    response = requests.post(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)

# get account details of a customer
def get_customer(customer_id: str = "378544"):

    url = f"https://portfoliomanager.energystar.gov/wstest/customer/{customer_id}"
    response = requests.get(url, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)



# update customer
def update_customer(customer_id: str = "378544"):
    # create customer url
    url = f"https://portfoliomanager.energystar.gov/wstest/customer/{customer_id}"

    # header
    headers = {"Content-Type": "application/xml"}


    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <customer>
    <phone>905-634-3888</phone>
    </customer>'''

    response = requests.put(url, headers=headers, data=body, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)


# get customer list from energy star
def get_customer_list():

    url = "https://portfoliomanager.energystar.gov/wstest/customer/list"
    response = requests.get(url, auth=HTTPBasicAuth('Renteknik-Group', 'Renteknik123'))
    print(response.content)




if __name__ == "__main__":
    print("Hello world!")
    # create_account_test()
    # get_account_details()
    # create_customer()
    # get_customer()
    # update_customer()
    get_customer_list()



# <response status="Ok">
#   <id>378484</id>
#   <links>
#     <link linkDescription="This is the GET url for this Account." link="/account" httpMethod="GET" />
#   </links>
# </response>
