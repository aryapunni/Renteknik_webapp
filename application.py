
from fastapi import FastAPI
import sqlalchemy
from typing import Optional, List
from pydantic import BaseModel, Field

app = FastAPI()


panpower = {}


# Schema for panpower measurements
class PanpowerMeasurement(BaseModel):
    device_id: int = Field(..., alias='device_id')
    device_name: str = Field(..., alias='device_name')
    measurement_time: str = Field(..., alias='measurement_time(UTC)')
    resolution: int = Field(..., alias='resolution(minutes)')
    site_id: int = Field(..., alias='site_id')
    site_name: str = Field(..., alias='site_name')
    current: float = Field(..., alias='current(A)')
    voltage: float = Field(..., alias='voltage(V)')
    power: float = Field(..., alias='power(W)')
    power_factor: float = Field(..., alias='power_factor')
    energy: float = Field(..., alias='energy(Wh)')


# schema for array of measurements
class PanpowerDictCover(BaseModel):
    measurements: List[PanpowerMeasurement]



# panpower post function
@app.post("/panpower/measurements")
async def panpower_format(datain: PanpowerDictCover):
    global panpower
    panpower = datain
    return datain


# panpower display function
@app.get("/panpower")
async def get_panpower():
    return {"panpower": panpower}


# Path parameter test function
@app.get("/item/{item_id}")
async def item(item_id: int):
    return {"item_id": item_id}


# FastAPI initial test function
@app.get("/")
async def root():
    return {"message": "Hello World"}
