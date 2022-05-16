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

def which_weekday(day: int):
    days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
    # print(f"Weekday is {days[day]}")
    return days[day]



def unique(value: list):
    output = []
    for val in value:
        if val not in output:
            output.append(val)
    return output

def create_ontime_list(ontime_interval: int):

    interval = {}
    day_val = 0
    start_val = 0
    end_val = 0
    day = []
    start = []
    end = []

    print("\nFollow this instructions for entering interval")
    print("\nMonday 0\nTuesday 1\nWednesday 2\nThursday 3\nFriday 4\nSaturday 5\nSunday 6\n\n")
    print("\nTime 0 to 24 Format\n")


    for i in range(0, ontime_interval):
        print(i)
        day_val, start_val, end_val = map(int, input("Enter the time: ").split())
        day.append(day_val)
        start.append(start_val)
        end.append(end_val)

    interval["day"] = day
    interval["start"] = start
    interval["end"] = end
    print(interval)
    return interval


def get_electrical_hierarchy():

    hierarchy = []
    n = int(input("\nEnter the number of elements: "))

    for i in range(0, n):
        element = input("\nEnter the electrical hierarchy: ")
        hierarchy.append(element)
    print(hierarchy)
    return hierarchy



def timestamp_datetime(time_stamp: str):
    fmt = "%Y-%m-%d %H:%M"

    date = datetime.strptime(time_stamp, fmt)
    return date


def ontime_or_offtime(ontime_intervals: dict, date: datetime):
    on_time_flag = 0
    index = 0
    start_time = 0
    end_time = 0
    current_time = 0
    weekday = which_weekday(date.weekday())
    if date.weekday() in ontime_intervals["day"]:
        index = ontime_intervals["day"].index(date.weekday())
        start_time = time(ontime_intervals["start"][index], 0, 0)
        end_time = time(ontime_intervals["end"][index], 0, 0)
        current_time = date.time()
        if(start_time <= current_time < end_time):
            print(f"\nDay: {date}")
            print(f"weekday: {weekday}")
            print("on TIME")
            on_time_flag = 1
        else:

            print(f"\nweekday: {weekday}")
            print("off TIME")
            on_time_flag = 0
    else:

        print(f"\nweekday: {weekday}")
        print("off_time")
        on_time_flag = 0


        # print(f"\nDATE:{date}\nindex: {index}\ndate.weekday() : {date.weekday()}\nWeekday: {weekday}")
        # print(f"start_time: {start_time}\nend_time: {end_time}\ncurrent_time: {date.time()}")


    return on_time_flag

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
    on_time_intervals = 0
    ontime_interval_list = []
    ontime_flag = 0


    cut_off_val = int(input("Enter the cut off value: "))

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
        print("\nList of column names : \n\n",list_of_column_names,"\n")


    # Getting csv indexes from user
    csv_index = get_electrical_hierarchy()



    on_time_intervals = int(input("\nEnter the number of on time intervals: "))
    ontime_interval_list = create_ontime_list(on_time_intervals)
    print(ontime_interval_list)

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


            ontime_flag = ontime_or_offtime(ontime_interval_list, date)
            if(ontime_flag):
                total_on_hours = total_on_hours + 1
                date_list.append(date)
                on_time.append(energy)
                off_time.append(0)
                off_time_cutoff.append(0)
                average.append(135)
            else:
                total_off_hours = total_off_hours + 1
                date_list.append(date)
                on_time.append(0)
                off_time.append(energy)
                off_time_cutoff.append(energy - cut_off_val)
                average.append(135)
            # print(ontime_flag)
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


    # Average On and Off consumption
    average_ontime_consumption = sum(on_time)/total_on_hours
    average_offtime_consumption = sum(off_time_cutoff)/total_off_hours

    # Off time percentage
    off_time_percentage = (average_offtime_consumption/average_ontime_consumption)*100


    # Daily off time target
    daily_offtime_target = average_ontime_consumption * 0.2


    print(f"\n\ntotal_off_hours: {total_off_hours} \ntotal_on_hours: {total_on_hours} \nmax_on_time: {max_on_time} \nmax_off_time: {max_off_time} \noff_time_percentage = (average_offtime_consumption/average_ontime_consumption)*100 = {off_time_percentage}\n")
    print(f"average_ontime_consumption =  sum(on_time)/total_on_hours = {average_ontime_consumption} \naverage_offtime_consumption = sum(off_time_cutoff)/total_off_hours = {average_offtime_consumption} \ndaily_offtime_target = average_ontime_consumption * 0.2 = {daily_offtime_target}\n\n")


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




    # graphs.generate_stacked_graph(meb_report, cut_off_val)
    graphs.generate_area_graph(meb_report, cut_off_val)
    graphs.generate_graph(meb_report_summary, cut_off_val)
