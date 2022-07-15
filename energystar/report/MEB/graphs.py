#!/usr/bin/env python3

import csv
from datetime import datetime
from datetime import time
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pathlib

# print(pathlib.Path().absolute())
path = pathlib.Path().absolute()




def generate_area_graph(meb_report, cut_off_val):

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x= meb_report['date'], y = meb_report['on_time'],
        name = 'On time',
        mode = 'lines',
        line=dict(width=0.5, color='darkgreen'),
        stackgroup = 'one'))
    fig3.add_trace(go.Scatter(
        x= meb_report['date'], y = meb_report['off_time_cutoff'],
        name = 'off_time',
        mode = 'lines',
        line=dict(width=0.1,color='red'),
        stackgroup = 'one'))

    fig3.update_layout(
        title = "MEB Report",
        title_font_size = 40, legend_font_size = 20,
        yaxis=dict(type='linear'), #,ticksuffix='%'
        # xaxis_tickformat = '%d %B (%a)<br>%Y', #'%d %B (%a)<br>%Y'
        width = 1600, height = 1000)
    fig3.update_xaxes(
        title_text = 'Month', fixedrange=True,
        title_font=dict(size=30, family='Verdana', color='black'),
        tickfont=dict(family='Calibri', color='darkred', size=25))
    fig3.update_yaxes(
        title_text = "Energy (kWh/h)", range = (0,1200),
        title_font=dict(size=30, family='Verdana', color='black'),
        tickfont=dict(family='Calibri', color='darkred', size=25))

    fig3.add_hline(y=cut_off_val, line_dash="dot",
              annotation_text="Off Time Target",
                   annotation_position="top left",
                   annotation=dict(font_size=15),
                   line_color="darkgreen")

    fig3.write_image(str(path) + "/graphs/figarea3.png", width=1500, height=1000)
    # fig3.write_image(path + "figarea3.png")
    # fig3.write_html("file3.html")
    fig3.show()



def generate_graph(meb_report, cut_off_val):

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x= meb_report['date'], y = meb_report['average_ontime'],
        name = 'On time',
        mode = 'lines', line=dict(width=0.1,color='darkgreen'),
        fill = 'tozeroy')) #tozeroy

    fig4.add_trace(go.Scatter(
        x= meb_report['date'], y = meb_report['average_offtime_cutoff'],
        name = 'off time',
        mode = 'lines', line=dict(width=0.1, color='lightgreen'),
        fill = 'tozeroy')) #tonexty

    fig4.add_hline(y=cut_off_val, line_dash="dot",
              annotation_text="Off Time Target",
                   annotation_position="top left",
                   annotation=dict(font_size=15),
                   line_color="darkgreen")

    # fig4.add_trace(go.Scatter(
    #     x= meb_report['date'], y = meb_report['off_time_cutoff'],
    #     name = 'off time - 150',
    #     mode = 'lines', line=dict(width=0.1, color='darkgreen'),
    #     fill = 'tonexty')) #tonexty

    fig4.update_layout(
        title = "MEB report",
        title_font_size=40, legend_font_size = 20,
        width = 1600, height = 1200)

    fig4.update_xaxes(
        title_text = 'March', fixedrange=True,
        title_font=dict(size=30, family='Verdana', color='black'),
        tickfont=dict(family='Calibri', color='darkred', size=25))

    fig4.update_yaxes(
        title_text = "Energy (kWh/h)", range = (0,1200), fixedrange=True,
        title_font=dict(size=30, family='Verdana', color='black'),
        tickfont=dict(family='Calibri', color='darkred', size=25))
    # fig4.write_image(path + "figarea4.png")

    fig4.write_image(str(path) + "/graphs/figarea.png", width=1500, height=1000)
    # fig4.write_html("file4.html")
    fig4.show()





# def generate_stacked_graph(meb_report, cut_off_val):
#     fig4 = go.Figure()
#     fig4.add_trace(go.Scatter(
#         x= meb_report['date'], y = meb_report['on_time'],
#         name = 'On time',
#         mode = 'lines', line=dict(width=0.1,color='yellowgreen'),
#         fill = 'tozeroy')) #tozeroy

#     fig4.add_trace(go.Scatter(
#         x= meb_report['date'], y = meb_report['off_time'],
#         name = 'off time',
#         mode = 'lines', line=dict(width=0.1, color='lightgreen'),
#         fill = 'tozeroy')) #tonexty

#     fig4.add_hline(y=cut_off_val, line_dash="dot",
#               annotation_text="Off Time Target",
#                    annotation_position="top left",
#                    annotation=dict(font_size=15),
#                    line_color="darkgreen")

#     fig4.add_trace(go.Scatter(
#         x= meb_report['date'], y = meb_report['off_time_cutoff'],
#         name = 'off time - 150',
#         mode = 'lines', line=dict(width=0.1, color='darkgreen'),
#         fill = 'tonexty')) #tonexty

#     fig4.update_layout(
#         title = "MEB report",
#         title_font_size=40, legend_font_size = 20,
#         width = 1600, height = 1000)

#     fig4.update_xaxes(
#         title_text = 'March', fixedrange=True,
#         title_font=dict(size=30, family='Verdana', color='black'),
#         tickfont=dict(family='Calibri', color='darkred', size=25))

#     fig4.update_yaxes(
#         title_text = "Energy (kWh)", range = (0,1200),
#         title_font=dict(size=30, family='Verdana', color='black'),
#         tickfont=dict(family='Calibri', color='darkred', size=25))
#     fig4.write_image(str(path) + "/graphs/figarea4.png")
#     # fig4.write_html("file4.html")
#     fig4.show()



# def generate_basicarea_graph(meb_report_summary, cut_off_val):

#     fig2 = px.area(meb_report_summary, x = 'date', y = ['average_offtime_cutoff', 'average_ontime'])

#     fig2.add_hline(y=cut_off_val)

#     fig2.update_layout(
#      title = "MEB Reports",
#      title_font_size = 40,
#      width = 1500, height = 900)

#     fig2.update_xaxes(
#      title_text = 'March',
#         range = (0, 200),
#      title_font=dict(size=30, family='Verdana', color='black'),
#      tickfont=dict(family='Calibri', color='darkred', size=25))

#     fig2.update_yaxes(
#      title_text = "Energy (kWh)",
#      range = (0,20000),
#      title_font=dict(size=30,family='Verdana',color='black'),
#      tickfont=dict(family='Calibri', color='darkred', size=25))


#     fig2.write_image(str(path) + "/graphs/figarea2.png")
#     # print(meb_report.groupby(['date']))
#     # fig1.write_image(path + "figarea1.png")
#     #
#     # fig2.write_html("file2.html")
#     # fig2.show()
