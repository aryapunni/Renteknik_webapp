
from fastapi import FastAPI, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session
from typing import Optional, List, Union, Optional
# from pydantic import BaseModel, Field, ValidationError, validator
from sql_app import models, schemas, crud
from sql_app.database import SessionLocal, engine
import json
import arc.arc
from config import settings
from arc.arc_get import get_asset_comprehensive_score, get_meter_list, asset_search, get_asset_list, get_asset_object_detail, get_fuel_category, get_meter_consumption_list, get_meter_consumption_detail, get_asset_aggregated_data, get_asset_score
# get_asset_aggregated_data, get_asset_score
from arc.arc_post import send_arc_consumption
import os
import logging
import sys



app = FastAPI()

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


# panpower pulse post function
@app.post("/panpower/panpowerpulse/{client}")
async def panpowerpulse_post(datain: schemas.PanpowerPulseDictCover, client: str, db: Session = Depends(get_db)):
    for data in datain.measurements:
        data.client = client
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
    for data in datain.measurements:
        data_1 = data.dict()
        print(json.dumps(data_1, indent=4, sort_keys=True))
        data.client = client
    crud.create_panpower(db=db, measurements=datain)
    return 200


# panpower10/12 post function
@app.post("/panpower/test")
async def panpower_post(datain: dict):
    print(json.dumps(datain, indent=4, sort_keys=True))
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
#------------------PANORAMIC POWER GET AND POST FUNCTIONS-------------------#



#------------------ARC INTEGRATION GET AND POST FUNCTIONS-------------------#
# Arc data posting link
@app.post("/arc/consumption/{client}/{leed_id}/{meter_id}")
async def post_consumption(meter_id: str, leed_id: str, client: str, datain: schemas.ArcEnergyDictCover, db: Session = Depends(get_db)):

    # Fetch data from the data base based on the leed id
    meta_data = crud.get_arc_metadata_leedid(db, leed_id)

    data = datain.dict()

    with open('data.json', 'a') as file:
        json.dump(data, file, indent = 4)
        file.write("\n")


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
async def post_co2_consumption(meter_id: str, leed_id: str, client: str, datain: schemas.ArcEnergyDictCover, db: Session = Depends(get_db)):

    # Fetch data from the data base based on the leed id
    meta_data = crud.get_arc_metadata_leedid(db, leed_id)

    data = datain.dict()

    with open('data.json', 'a') as file:
        json.dump(data, file, indent = 4)
        file.write("\n")


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

# Z3 Function
@app.post("/z3")
async def z3_post(data):
    print(data)

#------------------Z3 POST FUNCTION-------------------#

# FastAPI initial test function
@app.get("/")
async def root():
    return 200
