import csv
import pandas as pd
from datetime import datetime
from datetime import time
import jinja2
import pdfkit
from random import getrandbits, randint
import plotly.express as px
import numpy as np

def thousand_seperator(df, format):

    for column_name, item in df.iteritems():
        item = '{:,}'.format(column_name)
        # print(item)
        for val in item:
            # print(val)
            if isinstance(val, (float, int)):
                val = '{:,}'.format(val)
                print(val)
    return df

def plot_pi(df):
    fig = px.pie(df, values='Meter Final (kWh)', names='Suite ID', title='Energy Usage Onx')

    fig.write_image("figpi.png")
    fig.show()

def create_pdf(df):
    print(df)

    # Don't include the dataframe index in the html output,
    # add the appropriate css class, and don't draw the border.
    dfhtml = df.to_html(index=False, classes="table-title", border=False)

    #randint(0,100)

    # Load the template
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = env.get_template("tableTemplate.html")
    # pass df, title, message to the template.
    html_out = template.render(df=dfhtml,
                               title="Renteknik Group Inc.",
                               message="Energy Plots")

    # write the html to file
    with open("output.html", 'wb') as file_:
        file_.write(html_out.encode("utf-8"))

        # write the pdf to file
        pdfkit.from_string(html_out, output_path="output.pdf", css=["template.css"])


def pop_five_list(array_of_list):
    result = array_of_list[5:]

    return result


def suite_210_calc(array_of_list: list):
    feeder_i = array_of_list[0]
    feeder_j = array_of_list[1]
    # h4 = array_of_list[2]
    feeder_fa = array_of_list[3]
    feeder_fb = array_of_list[4]
    suite_220 = array_of_list[10]
    suite_250 = array_of_list[11]
    suite_270 = array_of_list[12]
    suite_280 = array_of_list[13]
    suite_300 = array_of_list[14]

    suite_210 = []
    feeders = 0
    suits = 0

    for i in range(len(feeder_fa)):
        if i == 0:
            suite_210.append("Suite   210")
        else:
            feeders = feeder_i[i] + feeder_j[i] + feeder_fa[i] + feeder_fb[i]
            suits = suite_220[i] + suite_250[i] + suite_270[i] + suite_280[i] + suite_300[i]
            suite_210.append(round(feeders - suits, 2))
    array_of_list.append(suite_210)
    return array_of_list


def array_of_list_from_dicts(dict1: dict, dict2: dict, dict3: dict, dict4: dict):
    array_of_list = []
    for key in dict1:
        array_element = [key, round(dict1[key], 2), round(dict2[key], 2), round(dict3[key], 2), round(dict4[key], 2)]
        array_element[0] = array_element[0].replace("(kWh)", "")
        array_of_list.append(array_element)
    return array_of_list


def cost_calc(energy_dict: dict, unit_cost: float):
    result_cost_dict = {}

    for key, value in energy_dict.items():
        result_cost_dict[key] = energy_dict[key] * unit_cost

    return result_cost_dict


def sum_of_two_dict(dict1: dict, dict2: dict):

    result_dict = {}
    for key in dict1:
        result_dict[key] = dict1[key] + dict2[key]
    return result_dict


def difference_of_two_dict(dict1: dict, dict2: dict):

    result_dict = {}
    for key in dict1:
        result_dict[key] = dict1[key] - dict2[key]
    return result_dict


def filter_month(dataframe, month:int):
    dataframe["Time stamp"] = pd.to_datetime(dataframe["Time stamp"])
    monthly_df = dataframe[dataframe["Time stamp"].dt.month == month]
    return monthly_df


def filter_months(dataframe, month:int):
    dataframe["Time stamp"] = pd.to_datetime(dataframe["Time stamp"])
    monthly_df = dataframe[dataframe["Time stamp"].dt.month < month]
    return monthly_df


def create_dict(dataframe):
    head = list(dataframe.columns)

    del(head[0])
    head_dict = {k:0 for k in head}
    return head_dict


def sum_of_dataframe(dataframe):
    head_dict = create_dict(dataframe)
    for column_name, items in dataframe.iteritems():
        if column_name in head_dict:
            head_dict[column_name] = dataframe[column_name].sum()

    return head_dict


def return_df():
    global result_dataframe
    return result_dataframe


if __name__ == "__main__":

    energy_head = []

    current_month = 4
    current_month_dict = {}
    prev_month_dict = {}
    sum_dict = {}
    cost_dict = {}
    unit_price = 0.1204
    array_list = []
    meter_start_dict = {}
    meter_final_dict = {}
    difference_dict = {}

    global result_dataframe


    onyx_data = pd.read_csv("energy.csv")


    # print(onyx_data)
    # current_month_df = filter_month(onyx_data, current_month)

    # current_month_dict = sum_of_dataframe(current_month_df)

    # prev_month_df = filter_month(onyx_data, current_month - 1)

    # prev_month_dict = sum_of_dataframe(prev_month_df)

    #-------------------------------------------------------#
    meter_start_df = filter_months(onyx_data, current_month - 1)
    meter_final_df = filter_months(onyx_data, current_month)

    meter_start_dict = sum_of_dataframe(meter_start_df)
    meter_final_dict = sum_of_dataframe(meter_final_df)

    difference_dict = difference_of_two_dict(meter_final_dict, meter_start_dict)



    cost_dict = cost_calc(difference_dict, unit_price)
    for key, val in cost_dict.items():
        print(key, val)

    array_list = array_of_list_from_dicts(meter_start_dict, meter_final_dict, difference_dict, cost_dict)
    array_list = suite_210_calc(array_list)
    # print(array_list)
    array_list = pop_five_list(array_list)

    # print("\n", array_list)

    result_dataframe = pd.DataFrame([array_list[i] for i in range(len(array_list))], columns=['Suite ID', 'Meter Start (kWh)', 'Meter Final (kWh)', 'Total Consumption (kWh)', 'Total Cost (USD)'])
    print(result_dataframe)


    # print(formatters)
    plot_pi(result_dataframe)

    pd.options.display.float_format = '{:,}'.format
    create_pdf(result_dataframe)
