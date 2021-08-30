
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

app = FastAPI()

# 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

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
        data.client = client
    crud.create_panpower(db=db, measurements=datain)
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
    meter_data = crud.get_arc_meterdata(db, meter_id)
    for data in datain.measurements:
        data.meter_id = meter_id
        data.leed_id = leed_id
        data.client = client
    electrical_hierarchy = meter_data.electrical_hierarchy
    time_data = {"duartion_format": "hours", "duration": 1, "time_zone": "Canada/Pacific"}
    send_arc_consumption(datain.dict(), electrical_hierarchy, time_data, settings.arc_primary_key)
    return 200


# Arc Meta data post link
@app.post("/arc/metadata")
async def post_arc_metadata(datain: schemas.ArcMetaData, db: Session = Depends(get_db)):
    for data in datain:
        print(data)
    crud.create_arc_metadata(db, datain)
    return 200


#------------------------------------------------------------------------------#
# Arc data posting link
@app.get("/arc/consumption")
async def get_consumption():
    return get_meter_list()
    # return get_meter_consumption_detail()
    # return get_asset_aggregated_data()
    # return get_asset_comprehensive_score()
    # return get_asset_score()
    # return asset_search()
    # return get_asset_list()
    # return get_asset_object_detail()
    # return get_fuel_category()
    # return get_meter_consumption_list()


# Arc Test Functions Get
# arc generate salt string
@app.get("/arc/saltstring")
async def get_saltstring():
    saltstring = arc.arc.generate_salt()
    return saltstring


# Arc test function to get
# database values
@app.get("/arc/table/{meter_id}")
async def get_arc_table(meter_id: str, db: Session = Depends(get_db)):
    val = crud.get_arc_meterdata(db=db, meter_id=meter_id)
    # print(val.leed_id)
    return val



#------------------ARC INTEGRATION GET AND POST FUNCTIONS-------------------#

# FastAPI initial test function
@app.get("/")
async def root():
    return {"message": "Hello World"}
