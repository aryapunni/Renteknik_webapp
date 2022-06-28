#!/usr/bin/env python3
import json
import itertools
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
        energy_kw = energy / 1000
        self.energy_sum += energy_kw
        self.energy_list.append(energy_kw)
        self.device_names.append(device_name)



if __name__ == "__main__":

    f = open('data_new.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)


    grouper = {}
    prev_key = data[0]["measurement_time"]
    for value in data:
        key = value['measurement_time']

        if key in grouper:
            energy_val = grouper[key]
        else:
            energy_val = energy_data()
            grouper[key] = energy_val

        energy_val.add_energy(value['energy'], value['device_name'])


    for item in grouper:
        print(f"\n{item}\n")
        # print(f"\n {item}\n{grouper[item].device_names}\n{grouper[item].energy_list}\n{grouper[item].energy_sum}")
        devicename = grouper[item].device_names
        energylist = grouper[item].energy_list
        energysum = grouper[item].energy_sum
        for (device, energy) in zip(devicename, energylist):
            print(f"{device}====>{energy}")
        print(f"\n{energysum}")

