import csv
import pandas as pd

def sum_of_energy(suite: dict, dataframe):
    suite['Energy Current Month [MWh]'] = dataframe['Suite 300 CHEP   (kWh)'].sum()/1000


if __name__ == "__main__":

    energy_head = []
    cost_head = []

    suite_300 = {}
    suite_180_east = {}
    suite_180_west = {}
    suite_101 = {}
    suite_130 = {}
    suite_250 = {}
    suite_125 = {}
    suite_220 = {}
    suite_280 = {}
    suite_270 = {}



    current_month = pd.read_csv("april.csv")
    prev_month = pd.read_csv("march.csv")
    cost_current_month = pd.read_csv("cost-april.csv")
    cost_prev_month = pd.read_csv("cost-march.csv")

    energy_head = list(current_month.columns)
    cost_head = list(cost_current_month.columns)

    print(energy_head)
    print(cost_head)
    # print(current_month)
    # print(prev_month)
    # print(cost_current_month)
    # print(cost_prev_month)
    suite_300['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_180_east['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_180_west['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_101['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_130['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_250['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_125['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_220['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_280['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    suite_270['Energy Current Month [MWh]'] = current_month['Suite 300 CHEP   (kWh)'].sum()/1000
    print(suite_300)
