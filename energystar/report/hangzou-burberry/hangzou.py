#!/usr/bin/env python3

import csv
import pandas as pd
from datetime import datetime
from datetime import time
import jinja2
import pdfkit
from random import getrandbits, randint
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import cufflinks as cf


# Convert Time stamp to datetime format
def time_stamp_format(df):

    df['Time stamp'] = pd.to_datetime(df['Time stamp'])
    return df

# Plot line graph for HVAC, Lighting, Power Panel, and BTU
# against time stamp
def plot_line(df, df2):

    # Converting Dataframe columns to Lists
    Time = df['Time stamp'].tolist()
    HVAC = df['HVAC Panel   (kWh)'].tolist()
    lighting = df['Lighting Panel   (kWh)'].tolist()
    power_panel = df['Power Panel (Power Outlets)   (kWh)'].tolist()
    BTU = df2['BTU Meter (kWh)'].tolist()

    # multiple subplots for each graph
    fig = make_subplots(rows=2, cols=2,  subplot_titles=("HVAC Panel (kWh)", "Lighting Panel (kWh)", "Power Panel (Power Outlets) (kWh)", "BTU Meter (kWh)"))

    fig.add_trace(go.Scatter(x=Time, y=HVAC), row=1, col=1)
    fig.add_trace(go.Scatter(x=Time, y=lighting), row=1, col=2)
    fig.add_trace(go.Scatter(x=Time, y=power_panel), row=2, col=1)
    fig.add_trace(go.Scatter(x=Time, y=BTU), row=2, col=2)

    # Limiting the size of the image
    fig.update_layout(height=600, width=1000, title_text="Energy Subplots", showlegend=False)
    # fig.show()

    fig.write_image("graphs/energy.jpeg")


# Function to Plot pi charts side by side
# Not used
def plot_pi_new(df):

    # Converting Dataframe columns to Lists
    labels = df['values'].tolist()
    week0 = df['week0'].tolist()
    week1 = df['week1'].tolist()

    # 2 sub plots for two pi charts
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    # Pi charts for two seperate weeks
    fig.add_trace(go.Pie(labels=labels, values=week0, name="Previous Week", title_text = "Previous Week"), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=week1, name="Current Week", title_text = "Current Week"), 1, 2)
    fig.update_layout(title_text="Weekly Energy Analysis Report", legend = dict(font = dict(family = "Courier", size = 13, color = "black")))
    # fig.show()
    fig.write_image("graphs/report.jpeg")


# Finding sum of energy consumption
def sum_energy_df(energy_df):

    # Creating list of all the columns
    col_list = list(energy_df)

    # Remove the timestamp from the list
    # for the sake of adding energy values
    col_list.remove('Time stamp')

    # Creating a new column for the total of all the columns
    energy_df['Total kWh'] = energy_df[col_list].sum(axis = 1)

    # return the resulting data frame
    # Dataframe with all sensor values and
    # sum of energy
    return energy_df

# plot pi chart for the dataframe passed
# df: dataframe passed
# name of the columnn that needs to be plotted
# name: heading of the graph
def plot_pi(df, week, name):
    fig = px.pie(df, values=week, names='values', title=name) #, titlefont_size=20

    fig.update_layout(height=1000, width=1000, legend = dict(font = dict(size = 20, color = "black"))) #family = "Courier",
    fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20)
    fig.write_image(f"graphs/{name}.jpeg")


# find the sum of the dataframe column vise
# used to make the summary table
def sum_df(df):
    val = df.sum(axis=0) #, skipna=True
    return val


# Creating a table with Co2 and BTU meter data
def create_co2_table(energy_df, co2_df):

    # Co2 data from panpower is sum of all the pulse inputs
    # We have to convert into average per day - /24
    co2_df['CO2 Sensor (PPM)'] = round(co2_df['CO2 Sensor   (ft³)']/24, 2)

    # BTU meter value is sum of heating meter and cooling meter value
    co2_df['BTU Meter (kWh)'] = energy_df['BTU Meter - Cooling   (kWh)'] + energy_df['BTU Meter Heat   (kWh)']

    # Droping the Column for co2 from panpower
    co2_df = co2_df.drop(columns = ['CO2 Sensor   (ft³)'])

    # returning the new co2 data
    return co2_df


#
def create_energy_table(energy_df):
    energy_df = energy_df.drop(columns = ['BTU Meter - Cooling   (kWh)', 'BTU Meter Heat   (kWh)'])
    return energy_df


def create_week0_table(week0_df):
    week0_df['BTU Meter (kWh)'] = week0_df['BTU Meter - Cooling   (kWh)'] + week0_df['BTU Meter Heat   (kWh)']
    week0_df = week0_df.drop(columns = ['BTU Meter - Cooling   (kWh)', 'BTU Meter Heat   (kWh)'])
    return week0_df

def create_summary_table(energy_df, co2_df, week0_df):

    week0 = []
    week1 = []
    energy_df = energy_df.drop(columns = ['Total kWh'])
    energy_df["BTU Meter (kWh)"] = co2_df["BTU Meter (kWh)"]
    week1_summary = sum_df(energy_df)
    week0_summary = sum_df(week0_df)
    for (data0, data1)  in zip(week0_summary, week1_summary):
        week0.append(data0)
        week1.append(data1)
    del week0[0], week1[0]
    print(week0, week1)
    summary = pd.DataFrame({'values' : ['HVAC Panel   (kWh)', 'Lighting Panel   (kWh)', 'Power Panel (Power Outlets)   (kWh)', 'BTU Meter (kWh)'],
                            'week0' : week0,
                            'week1' : week1})
    print(summary)
    return summary

def create_pdf(df, df2):

    # Don't include the dataframe index in the html output,
    # add the appropriate css class, and don't draw the border.
    dfhtml = df.to_html(index=False, classes="table-title", border=False)
    dfhtml2 = df2.to_html(index=False, classes="table-title", border=False)

    #randint(0,100)

    # Load the template
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = env.get_template("tableTemplate.html")
    # pass df, title, message to the template.
    html_out = template.render(df=dfhtml, df2=dfhtml2,
                               title="Renteknik Group Inc.",
                               message="Energy Plots")

    # write the html to file
    with open("output.html", 'wb') as file_:
        file_.write(html_out.encode("utf-8"))

        # write the pdf to file
        pdfkit.from_string(html_out, output_path="output.pdf", css=["template.css"])


def find_substring(list_string: list):
    sub = "panel"
    res = [i for i in list_string if sub in i.lower()]
    print(res)

if __name__ == "__main__":

    energy_data = pd.read_csv("energy.csv")
    co2_data = pd.read_csv("co2.csv")

    find_substring(energy_data.keys().to_list())

    co2_data = create_co2_table(energy_data, co2_data)
    print(co2_data)

    energy_data = create_energy_table(energy_data)

    energy_data = sum_energy_df(energy_df=energy_data)
    print(energy_data)

    week0_data = pd.read_csv("week0.csv")

    week0_data = create_week0_table(week0_data)
    print(week0_data)

    summary_table = pd.DataFrame()
    summary_table = create_summary_table(energy_data, co2_data, week0_data)

    plot_pi(summary_table, "week0", "Previous Week")
    plot_pi(summary_table,"week1", "Current Week")

    energy_data = time_stamp_format(energy_data)
    co2_data = time_stamp_format(co2_data)

    create_pdf(energy_data, co2_data)

    plot_pi_new(summary_table)
    plot_line(energy_data, co2_data)

    # create column name lists
    # create 6 different category of lists
    # Create 2 different big dfs week0 and week1
    # From this 2 different create 7 different dfs
    # --> week0 time hvac light plug-outlets total
    #    --> last row total of all columns
    # --> week1 time hvac light plug-outlets total
    #    --> last row total of all columns
    # --> week0 time co2  temp
    #    --> last row total/avg of all columns
    # --> week1 time co2 temp
    #    --> last row total/avg of all columns
    # --> week0 btu
    #    --> last row total of all btu data
    # --> week1 btu
    #    --> last row total of all btu data
    # --> -----  |week0|week1|%varience|
    #        HVAC|
    #    Lighting|
    # plug outlet|
    #     avg Co2|
    #    avg Temp|
    #
    #  -->Variance = ((week1 - week0) / week0 ) * 100
    #  Plot hourly graph of HVAC, Lighting, plug outlets
    #  Group all the data based on the date
    #  Create grouped dataframes and pass them to create pdf
    #  Based on the total table create the barchart
    #  Add bar charts and charts to the pdf
