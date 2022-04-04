
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from sqlalchemy.orm import Session
from typing import Optional, List, Union, Optional
from sql_app import models, schemas, crud
from sql_app.database import SessionLocal, engine
import json
import arc.arc
from config import settings
from arc.arc_get import get_asset_comprehensive_score, get_meter_list, asset_search, get_asset_list, get_asset_object_detail, get_fuel_category, get_meter_consumption_list, get_meter_consumption_detail, get_asset_aggregated_data, get_asset_score
# get_asset_aggregated_data, get_asset_score
from arc.arc_post import send_arc_consumption, send_arc_co2_consumption
import os
import logging
import sys
from datetime import datetime, timedelta, tzinfo
import pprint
from energystar import utils



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


origins = [
    "http://abacuslive.ca/z3",
    "https://abacuslive.ca/z3",
    "http://abacuslive.ca/z3:80",
    "https://abacuslive.ca/z3:443",
    "http://localhost/z3"
]

# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)

# logging.basicConfig(filename='abacus.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

models.Base.metadata.create_all(bind=engine)

# http://127.0.0.1:8000/arc/consumption/burberry/8000037879/11586622
# https://abacuslive.ca/arc/consumption/burberry/8000037879/11586622
# http://127.0.0.1:8000/panpower/panpower1012/{client}
#------------------PANORAMIC POWER GET AND POST FUNCTIONS-------------------#


# Now use the SessionLocal class we created in the sql_app/databases.py file to create a dependency
# We need to have an independent database connection per request
# use the same session through all the request and then close it after the request is finished
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/template/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("table.html", {"request": request, "id": id})


# panpower pulse post function
@app.post("/panpower/panpowerpulse/{client}")
async def panpowerpulse_post(datain: schemas.PanpowerPulseDictCover, client: str, db: Session = Depends(get_db)):

    metadata = crud.get_panpowermetadata_sitename(db, client)
    if metadata is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")


    print("----------------------Actual data----------------------")


    for data in datain.measurements:
        data_2 = data.dict()
        pprint.pprint(data_2)
        json_object = json.dumps(data_2, default=str, indent=4, sort_keys=True)

        with open("pan1012_actual.json", "a") as out_file:
            out_file.write(json_object)

    print("----------------------Time zone data----------------------")

    for data in datain.measurements:
        data.measurement_time = utils.change_timezone(data.measurement_time, metadata.timezone)
        data.client = client
        data_1 = data.dict()
        pprint.pprint(data_1)
        json_object = json.dumps(data_1, default=str, indent=4, sort_keys=True)

        with open("pan1012_timezone.json", "a") as out_file:
            out_file.write(json_object)

    crud.create_panpulse(db=db, measurements=datain)
    return 200



# panpower 42 post function
@app.post("/panpower/panpower42/{client}")
async def panpower42_post(datain: schemas.Pan42DictCover, client: str, db: Session = Depends(get_db)):
    for data in datain.measurements:
        data.client = client
    crud.create_pan42(db=db, measurements=datain)
    return 200



# panpower10/12 post function
@app.post("/panpower/panpower1012/{client}")
async def panpower1012_post(datain: schemas.PanPowerDictCover, client: str, db: Session = Depends(get_db)):


    metadata = crud.get_panpowermetadata_sitename(db, client)

    if metadata is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")


    print("----------------------Actual data----------------------")

    for data in datain.measurements:
        data_2 = data.dict()
        pprint.pprint(data_2)
        json_object = json.dumps(data_2, default=str, indent=4, sort_keys=True)

        with open("pan_actual.json", "a") as out_file:
            out_file.write(json_object)


    print("----------------------Time zone data----------------------")

    for data in datain.measurements:
        data.measurement_time = utils.change_timezone(data.measurement_time, metadata.timezone)
        data.client = client
        data_1 = data.dict()
        pprint.pprint(data_1)
        json_object = json.dumps(data_1, default=str, indent=4, sort_keys=True)

        with open("pan_timezone.json", "a") as out_file:
            out_file.write(json_object)


    crud.create_panpower(db=db, measurements=datain)


    return 200



# panpower10/12 post function
@app.post("/panpower/test")
async def panpower_post(datain: schemas.PanPowerDictCover): #datapulse: schemas.PanpowerPulseDictCover
    # print(json.dumps(datain, indent=4, sort_keys=True))
    # json_object = json.dumps(datain, indent=4, sort_keys=True)
    for data in datain.measurements:
        data_1 = data.dict()
        pprint.pprint(data_1)
        json_object = json.dumps(data_1, default=str, indent=4, sort_keys=True)

        with open("meb.json", "a") as out_file:
            out_file.write(json_object)

    for data in datain.measurements:
        data.measurement_time = utils.change_timezone(data.measurement_time, "America/Chicago")
        data_2 = data.dict()
        pprint.pprint(data_2)
        json_object = json.dumps(data_2, default=str, indent=4, sort_keys=True)

        with open("meb_timezone.json", "a") as out_file:
            out_file.write(json_object)

    return 200



# panpower10/12 data get function
@app.get("/panpower/panpower1012/{client}")
async def get_panpower1012(client: str, db: Session = Depends(get_db)):
    db_client = crud.get_panpower1012_client(db=db, client_name=client)
    if db_client is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")
    return  crud.get_panpower1012_client_data(db=db, client_name=client)



# panpower42 data get function
@app.get("/panpower/panpower42/{client}")
async def get_panpower42(client: str, db: Session = Depends(get_db)):
    db_client = crud.get_pan42_client(db=db, client_name=client)
    if db_client is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")
    return  crud.get_pan42_client_data(db=db, client_name=client)



# panpowerpulse data get function
@app.get("/panpower/panpowerpulse/{client}")
async def get_panpowerpulse(client: str, db: Session = Depends(get_db)):
    db_client = crud.get_panpowerpulse_client(db=db, client_name=client)
    if db_client is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")
    return  crud.get_panpowerpulse_client_data(db=db, client_name=client)


# Panpower Meta data post link
# input: PanpowerMetaData schema
@app.post("/panpower/metadata")
async def post_panpower_metadata(datain: schemas.PanpowerMetaData, db: Session = Depends(get_db)):
    print(datain)
    crud.create_panpower_metadata(db, datain)
    return 200


#------------------PANORAMIC POWER GET AND POST FUNCTIONS-------------------#


#------------------ENERGY STAR FUNCTIONS-------------------#


# Data fetching function for energy star
# input: from date, to date, client name, database name
@app.get("/energystar/{data}/{client}/{start_date}/{end_date}") #2021-09-17
async def energystar_data(data: str, client: str, start_date: str, end_date: str, db: Session = Depends(get_db)):

    trial_variable = utils.energy_star_report(db=db, data=data, client=client, start_date=start_date, end_date=end_date)
    return trial_variable


# Data fetching for 1-3 Rean drive
# Full month
@app.get("/energystar/fullmonth/{client}")
async def report_gen_1_3reandrive(request: Request, client: str, db: Session = Depends(get_db)):
    lists = []
    lists = utils.monthly_report_gen(client)
    print(lists)
    energy = lists[0]
    hot_water = lists[1]
    cold_water = lists[2]
    gas_meter = lists[3]

    utils.reandrive_barchart(energy=energy, hot_water=hot_water, cold_water=cold_water, gas_meter=gas_meter)

    # env = Environment(loader=FileSystemLoader('templates'))
    # template = env.get_template('table.html')
    # html = template.render(page_title_text='My report',
                       # title_text='Daily S&P 500 prices report')

    # return 200

    return templates.TemplateResponse("table.html", {"request": request, "energy": energy, "hot_water": hot_water, "cold_water": cold_water, "gas_meter": gas_meter}) #


#------------------ENERGY STAR FUNCTIONS-------------------#



#------------------ARC INTEGRATION GET AND POST FUNCTIONS-------------------#
# Arc data posting link
@app.post("/arc/consumption/{client}/{leed_id}/{meter_id}")
async def post_consumption(meter_id: str, leed_id: str, client: str, datain: schemas.ArcEnergyDictCover, db: Session = Depends(get_db)):

    # Fetch data from the data base based on the leed id
    meta_data = crud.get_arc_metadata_leedid(db, leed_id)

    data = datain.dict()

    # with open('data.json', 'a') as file:
    #     json.dump(data, file, indent = 4)
    #     file.write("\n")


    # print(json.dumps(datain, indent=4, sort_keys=True))

    # If that leed id is not available in the database
    # Send a 404 error
    if meta_data is None:
        print("There is no such Project in that Leed ID")
        raise HTTPException(status_code=404, detail="Leed ID not found")

    # If the data fetching was successfull proceed to send data to Arc
    for data in datain.measurements:
        data.meter_id = meter_id
        data.leed_id = leed_id
        data.client = client

    # Electrical hierarchy for filtering data
    electrical_hierarchy = meta_data.electrical_hierarchy

    # Timezone and time duration information for processing data
    time_data = {"duartion_format": meta_data.duration_format, "duration": meta_data.duration, "time_zone": meta_data.timezone}

    # Send data to Arc
    send_arc_consumption(db, datain.dict(), electrical_hierarchy, time_data)
    return 200



@app.post("/arc/co2_consumption/{client}/{leed_id}/{meter_id}")
async def post_co2_consumption(meter_id: str, leed_id: str, client: str, datain: schemas.ArcCo2DictCover, db: Session = Depends(get_db)):

    # Fetch data from the data base based on the leed id
    meta_data = crud.get_arc_metadata_leedid(db, leed_id)

    data = datain.dict()

    # with open('data.json', 'a') as file:
    #     json.dump(data, file, indent = 4)
    #     file.write("\n")


    # print(json.dumps(datain, indent=4, sort_keys=True))

    # If that leed id is not available in the database
    # Send a 404 error
    if meta_data is None:
        print("There is no such Project in that Leed ID")
        # raise HTTPException(status_code=404, detail="Leed ID not found")

    # If the data fetching was successfull proceed to send data to Arc
    for data in datain.measurements:
        data.meter_id = meter_id
        data.leed_id = leed_id
        data.client = client

    print(data)
    # # Electrical hierarchy for filtering data
    # electrical_hierarchy = meta_data.electrical_hierarchy

    # # Timezone and time duration information for processing data
    # time_data = {"duartion_format": meta_data.duration_format, "duration": meta_data.duration, "time_zone": meta_data.timezone}

    # # Send data to Arc
    send_arc_co2_consumption(db, datain.dict())
    return 200

# Arc create meter in ARC
@app.post("/arc/create_meter")
async def create_arc_meter(datain: schemas.ArcCreateMeter, db: Session = Depends(get_db)):

    # Create a meter in the specific leed ID
    arc.arc_post.create_meter_object(db=db, leed_id=datain.leed_id, client_name=datain.client_name, \
                                     meter_type=datain.meter_type, unit=datain.meter_unit, meter_id=datain.meter_id, \
                                     name=datain.meter_name, partner_details=datain.renteknik_meter)
    return 200



# Arc Meta data post link
# inputs are: leed_id, client_name, customer_uid
# electrical_hierarchy, timezone
# duration_format, duration
@app.post("/arc/metadata")
async def post_arc_metadata(datain: schemas.ArcMetaData, db: Session = Depends(get_db)):
    # Add metadata for a specific leed ID in the system
    crud.create_arc_metadata(db, datain)
    return 200


# --- Note that this link is only to be used when there is a key and token to be uploded directly --- #
# Arc Keys post link
# To create a new entry in the system if you have access token, refresh token, and time with you ready
# Different for different clients
@app.post("/arc/keys")
async def post_arc_key(datain: schemas.ArcKeyTable, db: Session = Depends(get_db)):
    datain.dict()
    crud.create_arc_keytable(db, datain)
    return 200


# Arc Meter data post link
# adding values to the meter table such as: meter_id, leed_id, customer_id
# meter_name, meter_type, meter_unit, renteknik_meter
@app.post("/arc/meter")
async def post_arc_meter(datain: schemas.ArcMeterTable, db: Session = Depends(get_db)):
    # Meter data for each Leed Ids
    crud.create_arc_metertable(db, datain)
    return 200


# Arc Meta data update link
# updates electrical hierarchy, timezone
# duration format and durations based on leed ID
@app.post("/arc/metadata/update")
async def update_arc_metadata(datain: schemas.ArcMetaData, db: Session = Depends(get_db)):
    crud.update_arcmetadata_leedid(db=db, leed_id=datain.leed_id, electrical_hierarchy=datain.electrical_hierarchy, timezone=datain.timezone, duration_format=datain.duration_format, duration=datain.duration)
    return 200


#------------------------------------------------------------------------------#



# Arc get links


# To get the arc consumption details
# leed_id: 800003789
# client_name: burberry
# meter_id: 11879657
@app.get("/arc/meter_consumption_list/{leed_id}/{client_name}/{meter_id}")
async def get_arc_meter_consumption_list(leed_id: str, client_name: str, meter_id: str, db: Session = Depends(get_db)):
    return get_meter_consumption_list(db=db, leed_id=leed_id, client_name=client_name, meter_id=meter_id)



# API to get fuel data from Arc
@app.get("/arc/fuel/{leed_id}/{client_name}")
async def get_arc_fuel(leed_id: str, client_name: str, db: Session = Depends(get_db)):
    return get_fuel_category(db=db, leed_id=leed_id, client_name=client_name)


# API to get asset object details data from Arc
@app.get("/arc/asset_object/{leed_id}/{client_name}")
async def get_arc_asset_object(leed_id: str, client_name: str, db: Session = Depends(get_db)):
    return get_asset_object_detail(db=db, leed_id=leed_id, client_name=client_name)



# API to get asset object details data from Arc
@app.get("/arc/asset_list/{leed_id}/{client_name}")
async def get_arc_asset_list(leed_id: str, client_name: str, db: Session = Depends(get_db)):
    return get_asset_list(db=db, leed_id=leed_id, client_name=client_name)



# API to get asset object details data from Arc
@app.get("/arc/asset_search/{leed_id}/{client_name}")
async def get_arc_asset_search(leed_id: str, client_name: str, db: Session = Depends(get_db)):
    return asset_search(db=db, leed_id=leed_id, client_name=client_name)


# API to get asset object details data from Arc
@app.get("/arc/asset_score/{leed_id}/{date}")
async def get_arc_asset_score(leed_id: str, date: str, db: Session = Depends(get_db)):
    return get_asset_score(leed_id=leed_id, date=date)



# API to get fuel data from Arc
@app.get("/arc/asset_comprehenive_score/{leed_id}/{date}")
async def get_arc_asset_comprehensive_score(leed_id: str, date: str, db: Session = Depends(get_db)):
    return get_asset_comprehensive_score(leed_id=leed_id, date=date)



# API to get fuel data from Arc
# startdate/enddate format - start_date="2020-08-29", end_date="2017-08-30" year-month-date
@app.get("/arc/asset_aggregated_data/{data_endpoint}/{leed_id}/{start_date}/{end_date}/{unit}")
async def get_arc_asset_aggregated_data(data_endpoint: str, leed_id: str, start_date: str, end_date: str, unit: str, db: Session = Depends(get_db)):
    return get_asset_aggregated_data(data_endpoint=data_endpoint, leed_id=leed_id, start_date=start_date, end_date=end_date, unit=unit)



# API to get fuel data from Arc ----> Not found
@app.get("/arc/meter_consumption/{leed_id}/{meter_id}/{client_name}")
async def get_arc_meter_consumption(leed_id: str, meter_id: str, client_name: str, db: Session = Depends(get_db)):
    return get_meter_consumption_detail(db=db, leed_id=leed_id, meter_id=meter_id, client_name=client_name)



# API to get fuel data from Arc
@app.get("/arc/meter_list/{leed_id}/{client_name}")
async def get_arc_meter_list(leed_id: str, client_name: str, db: Session = Depends(get_db)):
    return get_meter_list(db=db, leed_id=leed_id, client_name=client_name)



#------------------------------------------------------------------------------#


# Arc new client appplication registration adding
@app.get("/arc/new_client/{client}")
async def create_new_client(code: str, client: str, db: Session = Depends(get_db)):
    print(code, client)
    arc.arc.generate_newclient_auth2(db=db, client_name=client, code=code)
    return 200


#------------------ARC INTEGRATION GET AND POST FUNCTIONS-------------------#


#------------------Z3 POST FUNCTION-------------------#
@app.post("/z3")
async def z3_post(data: Request):
    req_info = await data.json()
    print(req_info)
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    server_response  = str(timestamp) + ", " + "0"

    return server_response

# Z3 Function
# for unknown json input:
# async def z3_post(data: Request):
#     req_info = await data.json()

# @app.post("/z3")
# async def z3_post(data: dict):
#     print(data)
#     now = datetime.now()
#     timestamp = int(datetime.timestamp(now))
#     server_response  = str(timestamp) + ", " + "0"

#     return server_response



    # return 200

#------------------Z3 POST FUNCTION-------------------#




#------------------Z3 GET FUNCTION-------------------#
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#
#------------------Z3 GET FUNCTION-------------------#



#------------------FILE DOWNLOAD FEATURE-------------------#

# Path to download files
@app.get("/download")
async def download():
    filepath = os.getcwd() + "/" + "first.json"
    return FileResponse(path=filepath, media_type="application/octet-stream", filename="first.json")


#------------------FILE DOWNLOAD FEATURE-------------------#



# FastAPI initial test function
@app.get("/")
async def root():
    return 200
