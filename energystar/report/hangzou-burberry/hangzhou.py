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

if __name__ == "__main__":

    energy_data = pd.read_csv("energy.csv")
    co2_data = pd.read_csv("co2.csv")

