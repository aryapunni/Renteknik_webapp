#!/usr/bin/env python3

from sql_app import models, schemas, crud
# import crc16
from itertools import groupby
from operator import itemgetter
import json
import itertools
import datetime
import requests
from time import sleep
from crc import CrcCalculator, Crc16
# import pprint


# Class Energy item
# Stores energy values and corresponding device name
class EnergyItem:
    def __init__(self, energy, device_name):
        self.energy = energy
        self.device_name = device_name




class energy_data:

    def __init__(self, energy_sum=0, device_names=None, energy_list=None):
        if device_names is None:
            device_names = []

        if energy_list is None:
            energy_list = []
        self.energy_sum = energy_sum
        self.device_names = device_names
        self.energy_list = energy_list

    def add_energy(self, energy, device_name):
        energy_kw = energy
        self.energy_sum += energy_kw
        self.energy_list.append(energy_kw)
        self.device_names.append(device_name)



# finding crc16 checksum based on the input string
def find_crc16(inputString: str):
    # converting input string to binary string
    binaryString = ''.join(format(ord(i), 'b') for i in inputString)
    binaryString = bytes(binaryString, 'utf-8')

    # finding crc16 checksum
    crc_calculator = CrcCalculator(Crc16.CCITT)
    checksum = crc_calculator.calculate_checksum(binaryString)
    checksum_hex = '{0:02x}'.format(checksum)

    # Finding the crc16 checksum with old python lib
    # print(type(binaryString))
    # crcString = crc16.crc16xmodem(binaryString)
    # hex_crc = '{0:02x}'.format(crcString)

    return checksum_hex

# Convert datetime object to string
def datetime_to_string(date):


    fmt = "%Y-%m-%d %H:%M:%-S"

    date.strftime(fmt)

    return date


# Creating the url encoded data for climacheck API
def create_climacheck_url(climacheck_dict: dict, time_stamp: str):

    # Renteknik UID
    uid = "U00185"

    # Length of the data that we are sending to the Climacheck
    number_of_datapoints = str(len(climacheck_dict))

    # Prefix of the url - uid + length of the datapoints + timestamp
    prefix = f"{uid},{number_of_datapoints},{time_stamp},"

    # Creating the datapoints for sending it to the Climacheck server
    climacheck_list = list(climacheck_dict.values())
    climacheck_str = ",".join([str(round(i, 2)) for i in climacheck_list])

    req_url = f"{prefix}{climacheck_str}"

    # Finding the crc16 checksum for the url encoded string
    crc = find_crc16(req_url)

    # final url string = uid + len-of-data + timestamp + data + crcchecksum
    req_url = f"{req_url},{crc}"
    return req_url


# The data to climacheck should be sent to
# climacheck in the right order based on time
# This function sorts the sensor values based on the time it was sent
def sort_climacheck_url(url_dict: dict):
    sorted_list = {k: v for k, v in sorted(url_dict.items(), key=lambda x: x[0])}
    for k, v in sorted_list.items():
        print(k, v)
    return sorted_list


#
def send_data_to_climacheck(climacheck_url_dict):

    url = "https://receiver.climacheck.com/"
    for date_time in climacheck_url_dict:
        raw_data = climacheck_url_dict[date_time]
        headers = {"Content-Type": "text/plain"}
        sleep(2)
        try:
            # print(url, raw_data, headers)
            r = requests.post(url=url, data=raw_data, headers=headers)
            print(r.text)
            # data = r.json()
            # print(f"requests data = {data}")
            # return data
        except Exception as e:
            print("[Errno {0}]".format(e))



    
def post_data(datain: schemas.PanPowerDictCover):
    climacheck_dict = {"50 HP Chiller Pump 5" : 0, "30 HP proc Chiller": 0, "Thermalcare Tower": 0,
                       "Tower #1": 0, "Tower #2": 0, "Tower #3": 0, "Tower #4": 0, "Tower #5": 0,
                       "40 HP Process 1":0, "40 HP Process 2":0, "40 HP Process 3":0,
                       "40 HP tower 1": 0, "40 HP tower 2":0}

    climacheck_url_dict = {}
    datain = datain.dict()
    grouper = {}


    for data in datain["measurements"]:
        # print(data)

        key = data["measurement_time"]

        # print(key)

        if key in grouper:
            energy_val = grouper[key]
        else:
            energy_val = energy_data()
            grouper[key] = energy_val

        energy_val.add_energy(round(data['power']/1000, 2), data['device_name'])


    for item in grouper:
        device_name_present = 0
        devicename = grouper[item].device_names
        energylist = grouper[item].energy_list

        # energysum = grouper[item].energy_sum

        for (device, energy) in zip(devicename, energylist):
            if device in climacheck_dict:
                device_name_present = 1
                print(f"{item}=====>{device}====>{energy}")
                climacheck_dict[device] = energy
        if device_name_present:
            climacheck_url_dict[item] = create_climacheck_url(climacheck_dict, datetime_to_string(item))
    print(climacheck_url_dict)
    climacheck_url_dict = sort_climacheck_url(climacheck_url_dict)
    send_data_to_climacheck(climacheck_url_dict=climacheck_url_dict)
