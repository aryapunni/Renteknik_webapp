#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime



if __name__ == "__main__":

    dates = []
    on_data = []
    off_data = []
    # constant = 150


    df = pd.read_excel(r'MEB Report.xlsm')

    print(f"{df}\n {type(df)}\n")

    date = df['Date']
    on = df['On']
    off = df['Off']

    for val in range(0, 31):
        dates.append(date[val])
        on_data.append(on[val])
        off_data.append(off[val])

        # print(date[val])
    print(date, on, off, dates, on_data, off_data)

    print(len(dates), len(on_data), len(off_data))
    print(dates, on_data, off_data)

    dataframe = {}
    dataframe["dates"] = dates
    dataframe["off_data"] = off_data
    dataframe["on_data"] = on_data
    df2 = pd.DataFrame(dataframe)

    print(f"============{dataframe}==============")

    sns.set()



    # Data
    # x=range(1,6)
    # y=[ [1,4,6,8,9], [2,2,7,10,12], [2,8,5,10,6] ]

    x = dates
    y = [on_data, off_data]
    # Plot
    plt.stackplot(x,y)
    plt.legend(loc='upper left')


    plt.show()

    plt.style.use('seaborn')
    df.plot.area()
    plt.xlabel('Time Stamp', fontsize=15)
    plt.ylabel('Energy', fontsize=15)
    plt.title('MEB Reports',fontsize=17)

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
    ax.legend(handles, labels)
    plt.show()


    plt.style.use('seaborn')
    df2.plot.area()
    plt.xlabel('Time Stamp', fontsize=15)
    plt.ylabel('Energy', fontsize=15)
    plt.title('MEB Reports',fontsize=17)

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
    ax.legend(handles, labels)
    plt.show()
