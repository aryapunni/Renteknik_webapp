
from fastapi import FastAPI
import sqlalchemy
from typing import Optional, List, Union, Optional
from pydantic import BaseModel, Field, ValidationError, validator

app = FastAPI()

# !!!global variables for development (Remove after testing)
var_panpower1012 = {}
var_panpower42 = {}
var_panpowerpulse = {}


# Schema for panpower pulse measurements
class PanpowerPulse(BaseModel):
    meter_id: int = Field(..., alias='METER_ID')
    meter_type: str = Field(..., alias='METER_TYPE')
    meter_name: str = Field(..., alias='METER_NAME')
    meter_unit: str = Field(..., alias='METER_UNIT')
    measurement_time: str = Field(..., alias='MEASUREMENT_TIME(UTC)')
    resolution: int = Field(..., alias='RESOLUTION(min)')
    site_id: int = Field(..., alias='SITE_ID')
    site_name: str = Field(..., alias='SITE_NAME')
    power: Union[float, str] = Field(..., alias='POWER(W)')
    energy: Optional[Union[float, str]] = Field(None, alias='ENERGY(Wh)')
    energy_k: Optional[Union[float, str]] = Field(None, alias='ENERGY(KWh)')
    energy_m: Optional[Union[float, str]] = Field(None, alias='ENERGY(MWh)')
    flow: Union[float, str] = Field(None, alias='FLOW')
    volume: Union[float, str] = Field(None, alias='VOLUME')


    # Function to validate the instance energy
    # @validator('energy')
    # def energy_format(cls, value):
    #    if not isinstance(value, float):
    #        return None


# schema for array of measurements(panpower pulse)
class PanpowerPulseDictCover(BaseModel):
    measurements: List[PanpowerPulse]


# Schema for panpower42 measurements
class Panpower42(BaseModel):
    device_id: int = Field(..., alias='device_id')
    device_name: str = Field(..., alias='device_name')
    measurement_time: str = Field(..., alias='measurement_time(UTC)')
    resolution: int = Field(..., alias='resolution(minutes)')
    site_id: int = Field(..., alias='site_id')
    site_name: str = Field(..., alias='site_name')
    phase: str = Field(..., alias='phase')
    current: float = Field(..., alias='current(A)')
    voltage: float = Field(..., alias='voltage(V)')
    power: float = Field(..., alias='power(W)')
    power_factor: float = Field(..., alias='power_factor')
    energy: float = Field(..., alias='energy(Wh)')
    reactive_power: float = Field(..., alias='reactive power(VAR)')
    consumed_active_energy: float = Field(..., alias='consumed active energy(Wh)')
    frequency: float = Field(..., alias='frequency(Hz)')


# schema for array of measurements(panpower 10/12)
class Panpower42DictCover(BaseModel):
    measurements: List[Panpower42]


# Schema for panpower10/12 measurements
class Panpower1012(BaseModel):
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


# schema for array of measurements(panpower 10/12)
class Panpower1012DictCover(BaseModel):
    measurements: List[Panpower1012]


# panpower pulse post function
@app.post("/panpower/panpowerpulse/client")
async def panpowerpulse_post(datain: PanpowerPulseDictCover):
    global var_panpowerpulse
    var_panpowerpulse = datain
    return datain


# panpower 42 post function
@app.post("/panpower/panpower42/client")
async def panpower42_post(datain: Panpower42DictCover):
    global var_panpower42
    var_panpower42 = datain
    return datain


# panpower10/12 post function
@app.post("/panpower/panpower1012/client")
async def panpower1012_post(datain: Panpower1012DictCover):
    global var_panpower1012
    var_panpower1012 = datain
    return datain


# !!!panpower10/12 display function
@app.get("/panpower/panpower1012/client")
async def get_panpower1012():
    return {"panpower": var_panpower1012}


# !!!panpower42 display function
@app.get("/panpower/panpower42/client")
async def get_panpower42():
    return {"panpower": var_panpower42}


# !!!panpower pulse display function
@app.get("/panpower/panpowerpulse/client")
async def get_panpowerpulse():
    return {"panpower": var_panpowerpulse}


# Path parameter test function
@app.get("/item/{item_id}")
async def item(item_id: int):
    return {"item_id": item_id}


# FastAPI initial test function
@app.get("/")
async def root():
    return {"message": "Hello World"}
