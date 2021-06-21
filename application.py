
from fastapi import FastAPI, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session
from typing import Optional, List, Union, Optional
# from pydantic import BaseModel, Field, ValidationError, validator
from sql_app import models, schemas, crud
from sql_app.database import SessionLocal, engine
import json
import arc.arc
from arc.arc_get import get_meter_list
from arc.arc_post import send_arc_consumption

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


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
    print(db_client)
    if db_client is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")
    return  crud.get_panpower1012_client_data(db=db, client_name=client)


# panpower42 data get function
@app.get("/panpower/panpower42/{client}")
async def get_panpower42(client: str, db: Session = Depends(get_db)):
    db_client = crud.get_pan42_client(db=db, client_name=client)
    print(db_client)
    if db_client is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")
    return  crud.get_pan42_client_data(db=db, client_name=client)


# panpowerpulse data get function
@app.get("/panpower/panpowerpulse/{client}")
async def get_panpowerpulse(client: str, db: Session = Depends(get_db)):
    db_client = crud.get_panpowerpulse_client(db=db, client_name=client)
    print(db_client)
    if db_client is None:
        print("there is no such client")
        raise HTTPException(status_code=404, detail="Client not found")
    return  crud.get_panpowerpulse_client_data(db=db, client_name=client)


#------------------PANORAMIC POWER GET AND POST FUNCTIONS-------------------#



#------------------ARC INTEGRATION GET AND POST FUNCTIONS-------------------#


# Arc Test Functions Get
# arc generate salt string
@app.get("/arc/saltstring")
async def get_saltstring():
    saltstring = arc.arc.get_access_token()
    data = arc.arc_get.get_meter_consumption_detail()
    return data


# Arc data posting link
@app.post("/arc/consumption/{client}/{leed_id}/{meter_id}")
async def post_consumption(meter_id: str, leed_id: str, client: str, datain: schemas.ArcEnergyDictCover):
    # print(meter_id, leed_id)
    # print(datain.dict())
    for data in datain.measurements:
        data.meter_id = meter_id
        data.leed_id = leed_id
        data.client = client
    send_arc_consumption(datain.dict())
    data = arc.arc_get.get_meter_consumption_detail()
    return "hello world"


#------------------ARC INTEGRATION GET AND POST FUNCTIONS-------------------#

# FastAPI initial test function
@app.get("/")
async def root():
    return {"message": "Hello World"}
