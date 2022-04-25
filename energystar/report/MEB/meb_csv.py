#!/usr/bin/env python3
import csv
from datetime import datetime
from datetime import time
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from statistics import mean
import graphs

def timestamp_datetime(time_stamp: str):
    fmt = "%Y-%m-%d %H:%M"

    date = datetime.strptime(time_stamp, fmt)
    return date
def average_ontime(ontime: list):
    print(ontime)


def unique(value: list):
    output = []
    for val in value:
        if val not in output:
            output.append(val)
    return output

def get_electrical_hierarchy():

    hierarchy = []
    n = int(input("Enter the number of elements: "))

    for i in range(0, n):
        element = input("Enter the electrical hierarchy: ")
        hierarchy.append(element)
    print(hierarchy)
    return hierarchy


if __name__ == "__main__":

# pylint: disable-msg=C0103

    csv_index = []
    # energy = 0
    # energy_new = 0
    on_time = []
    off_time = []
    off_time_cutoff = []
    date_list = []
    average = []
    MDP = []
    MDP_2 = []
    data_dict = {}
    data_dict_summary = {}
    dict_val = {}
    ontime_average = 0
    off_time_cutoff_average = 0
    nonzero_ontime = []
    nonzero_offtime_cutoff = []
    threshold = []
    cut_off_val = 150
    total_on_hours = 0
    total_off_hours = 0
    max_on_time = 0
    max_off_time = 0
    off_time_percentage = 0
    average_ontime_consumption = 0
    average_offtime_consumption = 0
    daily_offtime_target = 0
    hourly_offtime_target = 0
    average_ontime_list = []
    average_offtime_list = []

    filename = input("Enter the file name: ")

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        # converting the file to dictionary
        # by first convertingli to st
        # and then converting the list to dict
        dict_from_csv = dict(list(reader)[0])

        # making a list from the keys of the dict
        list_of_column_names = list(dict_from_csv.keys())

        # displaying the list of column names
        print("List of column names : ",
              list_of_column_names)


    # Getting csv indexes from user
    csv_index = get_electrical_hierarchy()






    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        for lines in reader:
            # extracting timestamp from csv
            timestamp = lines['\ufeff"Time stamp"']


            # convert timestamp to datetime format
            date = timestamp_datetime(timestamp)


            energy = 0

            for index in csv_index:
                energy = energy + float(lines[index])



            # Sum of MDP and MDP2 constitutes the total energy
            # energy = float(lines['MDP   (kWh)']) + float(lines['MDP2   (kWh)'])

            # print(f"energy: {energy}, energy new: {energy}")
            # extracting MDP and MDP2 from csv (Not necessary)
            # MDP.append(lines['MDP   (kWh)'])
            # MDP_2.append(lines['MDP2   (kWh)'])


            # If date.weekday() returns 5 or 6, those dates are weekends
            # If it is weekend append the energy value to the list off_time
            if date.weekday() > 4:
                # Computing total off hours
                total_off_hours = total_off_hours + 1

                # Creating a list with the timestamps (hourly data)
                date_list.append(date)

                # since this is weekend all energy data goes to off time
                on_time.append(0)
                off_time.append(energy)

                # off time time cutoff is off time energy - 150
                # 150 is a constant energy value which will not change at any time
                # there is no way that value can be reduced
                # So no need to analyse that
                off_time_cutoff.append(energy - 150)
                average.append(135)

            else:

                # All values other than weekend comes here
                # Extract time from the timestamp (remove date data)
                time_now = date.time()

                # setting On time and Off time for a weekday
                four_am = time(hour=4, minute=0, second=0)
                four_pm = time(hour=16, minute=0, second=0)

                # 4 am to 3.59 pm is ON time
                if four_am <= time_now < four_pm:
                    # Same things we did for OFF time/Weekend
                    # Just append values to On time not to Off time
                    total_on_hours = total_on_hours + 1
                    date_list.append(date)
                    on_time.append(energy)
                    off_time.append(0)
                    off_time_cutoff.append(0)
                    average.append(135)
                # 4 pm to 3 59 am on a weekday is Off time
                else:
                    # Same things we did for OFF time/Weekend
                    total_off_hours = total_off_hours + 1
                    date_list.append(date)
                    on_time.append(0)
                    off_time.append(energy)
                    off_time_cutoff.append(energy - 150)
                    average.append(135)


    # Create a list with non zero values in Ontime
    # Remove all the zeros from On time as it represents Off time
    nonzero_ontime = [i for i in on_time if i != 0]

    # Create a list with non zero values in Ontime
    # Remove all the zeros from On time as it represents Off time
    nonzero_offtime_cutoff = [i for i in off_time_cutoff if i != 0]

    # Average of on time values
    ontime_average = sum(nonzero_ontime)/len(nonzero_ontime)

    # Average of off time values
    off_time_cutoff_average = sum(nonzero_offtime_cutoff)/len(nonzero_offtime_cutoff)

    # Max value on the On time list and Off time List
    max_on_time = max(on_time)
    max_off_time = max(off_time)

    # Off time percentage
    off_time_percentage = (sum(off_time_cutoff)/sum(on_time))*100

    # Average On and Off consumption
    average_ontime_consumption = sum(on_time)/total_on_hours
    average_offtime_consumption = sum(off_time_cutoff)/total_off_hours

    # Daily off time target
    daily_offtime_target = (off_time_cutoff_average) * 0.2


    print(f"total_off_hours: {total_off_hours}, total_on_hours: {total_on_hours}\n max_on_time: {max_on_time} max_off_time: {max_off_time}\n off_time_percentage =  (sum(off_time_cutoff)/sum(on_time))*100 = {off_time_percentage}")
    print(f"average_ontime_consumption =  sum(on_time)/total_on_hours = {average_ontime_consumption},\n average_offtime_consumption = sum(off_time_cutoff)/total_off_hours = {average_offtime_consumption}\n, daily_offtime_target =  (off_time_cutoff_average) * 0.2 = {daily_offtime_target}")


    # Find threshold value for all the off time values
    # threshold = (offtime_cutoff/on time average) * 100
    # Create List with all the off time thresholds
    for value in off_time_cutoff:
        if value != 0:
            off_val = value
            off_time_threshold = (off_val/ontime_average) * 100
            threshold.append(off_time_threshold)
        else:
            threshold.append(value)


    # Creating a pandas Data frame using all the lists that we created
    # Data frame is used to create grapfs and csv files etc
    data_dict["threshold"] = threshold
    data_dict["date"] = date_list
    data_dict["on_time"] = on_time
    data_dict["off_time"] = off_time
    data_dict["off_time_cutoff"] = off_time_cutoff
    meb_report = pd.DataFrame(data_dict)
    # print(meb_report.to_markdown())
    # meb_report.to_csv("meb_report.csv")


    # Creating another Pandas data frame with just dates, without hour data
    data_dict_summary["date"] = [date.date() for date in date_list]
    data_dict_summary["on_time"] = on_time
    data_dict_summary["off_time"] = off_time
    data_dict_summary["off_time_cutoff"] = off_time_cutoff


    meb_report_summary = pd.DataFrame(data_dict_summary)

    meb_report_summary = meb_report_summary.groupby(["date"], as_index=True).sum()

    on_time_summary_avg = meb_report_summary['on_time'].tolist()
    on_time_summary_avg = [i for i in on_time_summary_avg if i != 0]


    ontime_average = sum(on_time_summary_avg)/len(on_time_summary_avg)


    meb_report_summary["date"] = unique(data_dict_summary["date"])

    threshold.clear()

    for index, row in meb_report_summary.iterrows():
        off_val = row['off_time_cutoff']
        off_time_threshold = (off_val/ontime_average) * 100
        threshold.append(off_time_threshold)
        date = row["date"]
        if date.weekday() > 4:
            average_offtime_list.append(row["off_time_cutoff"]/24)
            average_ontime_list.append(0)
        else:
            average_offtime_list.append(row["off_time_cutoff"]/12)
            average_ontime_list.append(row["on_time"]/12)

        # print(row)
        # print(date)
    meb_report_summary["threshold"] = threshold
    meb_report_summary["average_ontime"] = average_ontime_list
    meb_report_summary["average_offtime_cutoff"] = average_offtime_list



    print(meb_report_summary.to_markdown())




    graphs.generate_stacked_graph(meb_report, cut_off_val)
    graphs.generate_area_graph(meb_report, cut_off_val)
    graphs.generate_graph(meb_report_summary, cut_off_val)
