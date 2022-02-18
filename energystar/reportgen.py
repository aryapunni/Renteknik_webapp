#!/usr/bin/env python3

# import pandas as pd
# import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
import numpy as np


if __name__ == "__main__":

    print("hello world")
    df = pd.DataFrame()
    df['Question'] = ["Q1", "Q2", "Q3", "Q4"]
    df['Charles'] = [3, 4, 5, 3]
    df['Mike'] = [3, 3, 4, 4]

    title("Professor Criss's Ratings by Users")
    xlabel('Question Number')
    ylabel('Score')

    c = [2.0, 4.0, 6.0, 8.0]
    m = [x - 0.5 for x in c]

    xticks(c, df['Question'])

    bar(m, df['Mike'], width=0.5, color="#91eb87", label="Mike")
    bar(c, df['Charles'], width=0.5, color="#eb879c", label="Charles")

    legend()
    axis([0, 10, 0, 8])
    savefig('barchart.png')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    # pdf.cell(60)
    # pdf.cell(75, 10, "A Tabular and Graphical Report of Professor Criss's Ratings by Users Charles and Mike", 0, 2, 'C')
    # pdf.cell(90, 10, " ", 0, 2, 'C')
    # pdf.cell(-40)
    # pdf.cell(50, 10, 'Question', 1, 0, 'C')
    # pdf.cell(40, 10, 'Charles', 1, 0, 'C')
    # pdf.cell(40, 10, 'Mike', 1, 2, 'C')
    # pdf.cell(-90)
    # pdf.set_font('arial', '', 12)

    # for i in range(0, len(df)):
    #     pdf.cell(50, 10, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
    #     pdf.cell(40, 10, '%s' % (str(df.Mike.iloc[i])), 1, 0, 'C')
    #     pdf.cell(40, 10, '%s' % (str(df.Charles.iloc[i])), 1, 2, 'C')
    #     pdf.cell(-90)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-30)
    pdf.image('barchart.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.output('test.pdf', 'F')

    n= 6

    m1 = (0.10,0.12,0.10,0.11,0.14,0.10)
    m2 = (0.21,0.21,0.20,0.22,0.20,0.21)
    m3 = (0.29,0.27,0.28,0.24,0.23,0.23)
    m4 = (0.41,0.39,0.35,0.37,0.41,0.40)
    x = [1,2,3,4,5,6]

    fig, ax = plt.subplots()

    index = np.arange(n)
    bar_width = 0.2

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    r1 = ax.bar(index, m1, bar_width,
                alpha=opacity,
                color='b',
                error_kw=error_config)

    r2 = ax.bar(index + bar_width, m2, bar_width,
                alpha=opacity,
                color='r',
                error_kw=error_config)

    r3 = ax.bar(index + bar_width+ bar_width, m3, bar_width,
                alpha=opacity,
                color='y',
                error_kw=error_config)
    r4 = ax.bar(index + bar_width+ bar_width+ bar_width, m4, bar_width,
                alpha=opacity,
                color='c',
                error_kw=error_config)
    plt.xlabel('D')
    plt.ylabel('Anz')
    plt.title('Th')

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

    ax1.bar(x,m1, 0.2)  #% thickness=0.2
    ax2.bar(x,m2, 0.2)
    ax3.plot(x,m3)
    ax4.plot(x,m4)

    plt.tight_layout()
    plt.show()
