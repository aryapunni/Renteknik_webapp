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
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
energy =   ["23,740", "23,680", "26,380","24,700", 0, 0, 0, 0, 0, 0, 0, 0]
hot_water =   ["2,368", "1,878", "1,336", "339", 0, 0, 0, 0, 0, 0, 0, 0]
cold_water =   ["6,296", "8,408", "10,484", "7,400", 0, 0, 0, 0, 0, 0, 0, 0]
gas_meter =   ["87,550", "65,660", "129,600", "109,900", 0, 0, 0, 0, 0, 0, 0, 0]
df = pd.DataFrame([{"Months":months[i],
                    "Electricity(kWh)":energy[i],
                    "Hot Water(ft3)":hot_water[i],
                    "Cold Water(ft3)":cold_water[i],
                    "Gas Meter(ft3)":gas_meter[i]} for i in range(12)])[['Months','Electricity(kWh)','Hot Water(ft3)','Cold Water(ft3)','Gas Meter(ft3)']]


# Don't include the dataframe index in the html output,
# add the appropriate css class, and don't draw the border.
dfhtml = df2.to_html(index=False, classes="table-title", border=False)

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

