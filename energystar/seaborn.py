#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import csv

def write_csv(fields: list, rows: dict, name: str):

    filename = f"{name}.csv"
    print(fields, rows, name)
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        for val in rows.items():
            row = [list(val)]

            # writing the data rows
            csvwriter.writerows(row)

if __name__ == "__main__":

    row = {'Jan': "452", 'Feb': "300", 'Mar': "200", 'Apr': "450", 'May': "400", 'Jun': "0", 'Jul': "0", 'Aug': "0", 'Sep': "0", 'Oct': "0", 'Nov': "0", 'Dec': "0"}

    fileds = ["months", "energy"]

    write_csv(fileds, row, "energy")
