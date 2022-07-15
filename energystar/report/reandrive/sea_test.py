#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def reandrive_barchart(energy: dict, hot_water: dict, cold_water: dict, gas_meter: dict):

    months = list(energy.keys())

    # energy = [int(energy[k]) for k in months]
    # print(energy)
    # sns.barplot(x=months, y=energy, dodge=False)
    # plt.title("Energy(kWh)")
    # plt.ylim(20000, 28000)
    # plt.xlabel("Months")
    # plt.ylabel("Energy(kWh)")
    # plt.savefig('quantiphi/energy.png')


    # hot_water = [int(hot_water[k]) for k in months]
    # print(hot_water)
    # sns.barplot(x=months, y=hot_water)
    # plt.title("Hot Water(ft3)")
    # plt.ylim(0, 2500)
    # plt.xlabel("Months")
    # plt.ylabel("Hot Water(ft3)")
    # plt.savefig('quantiphi/hot_water.png')


    cold_water = [int(cold_water[k]) for k in months]
    sns.barplot(x=months, y=cold_water, dodge=False)
    print(cold_water)
    plt.ylim(3000, 11000)
    plt.title("Cold Water(ft3)")
    plt.xlabel("Months")
    plt.ylabel("Cold Water(ft3)")
    plt.savefig('quantiphi/cold_water.png')


    # gas_meter = [int(gas_meter[k]) for k in months]
    # print(gas_meter)
    # plt.title("Natural Gas(ft3)")
    # plt.ylim(10000, 140000)
    # plt.xlabel("Months")
    # plt.ylabel("Natural Gas(ft3)")
    # sns.barplot(x=months, y=gas_meter, dodge=False)
    # plt.savefig('quantiphi/gas_meter.png')


if __name__ == "__main__":
    energy = {'Jan': "23740", 'Feb': "23680", 'Mar': "26380", 'Apr': "24700", 'May': "20950", 'Jun': "0", 'Jul': "0", 'Aug': "0", 'Sep': "0", 'Oct': "0", 'Nov': "0", 'Dec': "0"}
    hot_water = {'Jan': "2368", 'Feb': "1878", 'Mar': "1336", 'Apr': "339", 'May': "1059", 'Jun': "0", 'Jul': "0", 'Aug': "0", 'Sep': "0", 'Oct': "0", 'Nov': "0", 'Dec': "0"}
    cold_water = {'Jan': "6296", 'Feb': "8408", 'Mar': "10484", 'Apr': "7400", 'May': "3891", 'Jun': "0", 'Jul': "0", 'Aug': "0", 'Sep': "0", 'Oct': "0", 'Nov': "0", 'Dec': "0"}
    gas_meter = {'Jan': "87550", 'Feb': "65660", 'Mar': "129600", 'Apr': "109900", 'May': "51400", 'Jun': "0", 'Jul': "0", 'Aug': "0", 'Sep': "0", 'Oct': "0", 'Nov': "0", 'Dec': "0"}


    reandrive_barchart(energy, hot_water, cold_water, gas_meter)
