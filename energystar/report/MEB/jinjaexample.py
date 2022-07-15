#!/usr/bin/env python3

import pandas as pd
import jinja2
import pdfkit
from random import getrandbits, randint

# pdfkit is just a wrapper for whktmltopdf. you need to install wkhtml and have it on the path
# alternatively, you can move wkhtmltoimage.exe, wkhtmltopdf.exe and wkhtmltox.dll into the working directory

# Create some data
def random_hex(length=10):
    return '%0x' % getrandbits(length * 4)



data = [['Maximum Production Daily Consumption (kWh/h)', 1194.21],
        ['Non-switchable load (kW)', 150],
        ['Off-Time Percentage (%)', 21.56],
        ['Hourly Average On-Time Consumption (kWh/h)', 714.99],
        ['Hourly Average Off-Time Consumption (kWh/h)', 154.20],
        ['Off-Time Target Consumption (kWh/h)', 142.99],]
df = pd.DataFrame(data, columns = ['Category', 'Value'])


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
                           message="")

# write the html to file
with open("output.html", 'wb') as file_:
    file_.write(html_out.encode("utf-8"))

# write the pdf to file
pdfkit.from_string(html_out, output_path="output.pdf", css=["template.css"])

