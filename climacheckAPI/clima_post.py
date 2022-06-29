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



def find_crc16(inputString: str):
    binaryString = ''.join(format(ord(i), 'b') for i in inputString)
    binaryString = bytes(binaryString, 'utf-8')
    print(type(binaryString))
    # crcString = crc16.crc16xmodem(binaryString)
    # hex_crc = '{0:02x}'.format(crcString)
    crc_calculator = CrcCalculator(Crc16.CCITT)
    checksum = crc_calculator.calculate_checksum(binaryString)
    checksum_hex = '{0:02x}'.format(checksum)

    print(f"checksum new lib: {checksum}, {checksum_hex}")
    return checksum_hex

def datetime_to_string(date):

    fmt = "%Y-%m-%dT%H:%M:%S"

    date.strftime(fmt)
    return date

def create_climacheck_url(climacheck_dict: dict, time_stamp: str):
    # print(time_stamp, "\n", climacheck_dict)

    url = "https://receiver.climacheck.com/"
    uid = "U00185"
    number_of_datapoints = str(len(climacheck_dict))
    prefix = f"{url}{uid},{number_of_datapoints},{time_stamp}"
    climacheck_list = list(climacheck_dict.values())
    climacheck_str = ",".join([str(round(i, 2)) for i in climacheck_list])
    # print(climacheck_str)
    req_url = f"{prefix}{climacheck_str}"
    crc = find_crc16(req_url)
    req_url = f"{req_url},{crc}"
    print(req_url, crc)
    return req_url

def sort_climacheck_url(url_dict: dict):
    sorted_list = {k: v for k, v in sorted(url_dict.items(), key=lambda x: x[0])}
    for k, v in sorted_list.items():
        print(k, v)
    return sorted_list



def send_data_to_climacheck(climacheck_url_dict):
    for date_time in climacheck_url_dict:
        url = climacheck_url_dict[date_time]
        sleep(2)
        try:
            r = requests.post(url=url)
            print(r.text)
            data = r.json()
            print(f"requests data = {data}")
            # return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))



    
def post_data(datain: schemas.PanPowerDictCover):
    climacheck_dict = {"50 HP Chiller Pump 5" : 0, "30 HP Process Pump": 0, "Thermalcare Tower": 0,
                       "Tower #1": 0, "Tower #2": 0, "Tower #3": 0, "Tower #4": 0, "Tower #5": 0,
                       "40 HP Process 1":0, "40 HP Process 2":0, "40 HP Process 3":0,
                       "40 HP tower 1": 0, "40 HP tower 2":0}

    climacheck_url_dict = {}
    datain = datain.dict()
    grouper = {}


    for data in datain["measurements"]:
        # print(data)

        key = data["measurement_time"]

        if key in grouper:
            energy_val = grouper[key]
        else:
            energy_val = energy_data()
            grouper[key] = energy_val

        energy_val.add_energy(data['energy'], data['device_name'])


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


                # Too many repeated iterations of sending data
                # Have to remove those iterartions and make it send only once

