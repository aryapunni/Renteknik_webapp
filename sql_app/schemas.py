from typing import Optional, List, Union
from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from datetime import datetime



# function to find whether input in float or string
# if float: o/p = 1, if string: o/p = 0
def float_or_string(value):
    if isinstance(value, float):
        return 1
    elif isinstance(value, str):
        return 0

# general metadata
# site name: name given in the panpower database
# client : Name of the client as of the panoramic database
# electrical_hierarchy - strings seperated by space
# time_zone: time zone of the project locattion
# api_name: panpower post api
# device sensor types: pan1012 or pan 42 or pulse
# remarks: general remarks if any
class PanpowerMetaData(BaseModel):
    site_name: str
    client_name: str
    site_uid: str
    electrical_hierarchy: str
    timezone: str
    dst: str
    api_name: str
    device_sensor_types: str
    remarks: str

    class Config:
        orm_mode = True


# Schema for panpower pulse measurements
class PanpowerPulse(BaseModel):
    client: Optional[str]
    meter_id: int = Field(..., alias='METER_ID')
    meter_type: str = Field(..., alias='METER_TYPE')
    meter_name: str = Field(..., alias='METER_NAME')
    meter_unit: str = Field(..., alias='METER_UNIT')
    measurement_time: Union[str, datetime] = Field(..., alias='MEASUREMENT_TIME(UTC)')
    resolution: int = Field(..., alias='RESOLUTION(min)')
    site_id: int = Field(..., alias='SITE_ID')
    site_name: str = Field(..., alias='SITE_NAME')
    power: Union[float, str] = Field(..., alias='POWER(W)')
    energy: Optional[Union[float, str]] = Field(None, alias='ENERGY(Wh)')
    energy_k: Optional[Union[float, str]] = Field(None, alias='ENERGY(KWh)')
    energy_m: Optional[Union[float, str]] = Field(None, alias='ENERGY(MWh)')
    flow: Union[float, str] = Field(None, alias='FLOW')
    volume: Union[float, str] = Field(None, alias='VOLUME')

    class Config:
        orm_mode = True

# validator function to check input value coming in are N/A or a float
# If it is a N/A ie a string it will conver to None
    @validator('power', 'energy', 'energy_k', 'energy_m', 'flow', 'volume')
    def float_string_validator(cls, value):
        result = float_or_string(value)
        if result == 0:
            return None
        return value

# validator function to check input value coming in are N/A or a float
    # If it is a N/A ie a string it will conver to None
    @validator('measurement_time')
    def datetime_converter(cls, value):
        # Time format
        fmt = "%Y-%m-%dT%H:%M:%S"

        # Removing the extra z from the panpower data
        # Inorder to make the date format compatible with Arc
        if isinstance(value, str):
            if value.endswith('Z'):
                value = value[:-1]

        value = datetime.strptime(value, fmt)

        return value



# schema for array of measurements(panpower pulse)
class PanpowerPulseDictCover(BaseModel):
    measurements: List[PanpowerPulse]


# Base class for panpower(Testing)
class PanPower(BaseModel):
    client: Optional[str]
    device_id: int = Field(..., alias='device_id')
    device_name: str = Field(..., alias='device_name')
    measurement_time: Union[str, datetime] = Field(..., alias='measurement_time(UTC)')
    resolution: int = Field(..., alias='resolution(minutes)')
    site_id: int = Field(..., alias='site_id')
    site_name: str = Field(..., alias='site_name')
    current: float = Field(..., alias='current(A)')
    voltage: float = Field(..., alias='voltage(V)')
    power: float = Field(..., alias='power(W)')
    power_factor: float = Field(..., alias='power_factor')
    energy: float = Field(..., alias='energy(Wh)')

    class Config:
        orm_mode = True


    # validator function to check input value coming in are N/A or a float
    # If it is a N/A ie a string it will conver to None
    @validator('measurement_time')
    def datetime_converter(cls, value):
        # Time format
        fmt = "%Y-%m-%dT%H:%M:%S"

        # Removing the extra z from the panpower data
        # Inorder to make the date format compatible with Arc
        if isinstance(value, str):
            if value.endswith('Z'):
                value = value[:-1]

        value = datetime.strptime(value, fmt)
        return value




# schema for array of measurements(panpower)
class PanPowerDictCover(BaseModel):
    measurements: List[PanPower]


# Sub class of panpower(Testing)
class PanPower42(PanPower):
    phase: str = Field(..., alias='phase')
    reactive_power: float = Field(..., alias='reactive power(VAR)')
    consumed_active_energy: float = Field(..., alias='consumed active energy(Wh)')
    frequency: Optional[float] = Field(None, alias='frequency(Hz)')

    class Config:
        orm_mode = True


# schema for array of measurements(pan42)
class Pan42DictCover(BaseModel):
    measurements: List[PanPower42]


# schema for arc data Energy consumption
class ArcEnergyConsumption(BaseModel):
    client: Optional[str]
    device_id: Optional[str]
    leed_id: Optional[str]
    device_name: str
    meter_id: Optional[str]
    measurement_time: str = Field(..., alias='measurement_time(UTC)')
    energy: float = Field(..., alias='energy(Wh)')


# schema for arc data CO2
class ArcCo2Consumption(BaseModel):
    client: Optional[str]
    leed_id: Optional[str]
    meter_id: Optional[int]
    measurement_time: str = Field(..., alias='MEASUREMENT_TIME(UTC)')
    energy: Optional[Union[float, str]] = Field(..., alias='ENERGY(Wh)')
    flow: Optional[Union[float, str]] = Field(..., alias='FLOW')
    volume: Optional[Union[float, str]] = Field(..., alias='VOLUME')


    # validator function to check input value coming in are N/A or a float
    # If it is a N/A ie a string it will conver to None
    @validator('flow', 'volume')
    def float_string_validator(cls, value):
        result = float_or_string(value)
        if result == 0:
            return None
        return value




# schema for ArcEnergyConsumption
class ArcEnergyDictCover(BaseModel):
    measurements: List[ArcEnergyConsumption]



# schema for ArcCo2Consumption
class ArcCo2DictCover(BaseModel):
    measurements: List[ArcCo2Consumption]


# schema for Arc metadata
# Leed ID of the project From Arc
# Client name identifier from Panpower - can be taken from panpower client name
# customer_uid: the id coming up on the url when we open a panpower project
# One project can have one leed id and multiple meters and multiple meter types
# electrical_hierarchy - strings seperated by space
# time_zone: time zone of the project locattion
# duration_format: days, hours, or minutes
# duration: duration as an integer, such as one day or hour etc
class ArcMetaData(BaseModel):
    leed_id: str
    client_name: str
    customer_name: str
    customer_uid: str
    electrical_hierarchy: str
    timezone: str
    duration_format: str
    duration: str

    class Config:
        orm_mode = True


# Table for storing Arc access tokens and refresh tokens
# client_name - client name of this purticular client - such as magna or torro or burberry
# Note that for each different projects we need different access and refresh tokens
# access_token and refresh_token for this purticular project
# time: last time when we generated a new access and refresh token
# Note that the access token expires after 10 hours
# so we have to generate one every 10 hours
class ArcKeyTable(BaseModel):
    client_name: str
    access_token: str
    refresh_token: str
    current_time: str

    class Config:
        orm_mode = True


# Table for storing Arc access tokens and refresh tokens
# leed_id - leed id of this purticular project
# client_name - client name of this purticular project
# Note that for each different projects we need different access and refresh tokens
# access_token and refresh_token for this purticular project
# time: last time when we generated a new access and refresh token
# Note that the access token expires after 10 hours
# so we have to generate one every 10 hours
class ArcMeterTable(BaseModel):
    meter_id: str
    leed_id: str
    customer_id: str
    meter_name: str
    meter_type: str
    meter_unit: str
    renteknik_meter: str
    duration_format: str
    duration: str

    class Config:
        orm_mode = True




# Table for storing Arc access tokens and refresh tokens
# leed_id - leed id of this purticular project -- FOR ARC
# client_name - client name of this purticular project -- FOR ABACUS
# meter_type - The types of meter provided in arc
# example: for electricity meter: 46 -- FOR ARC
# meter_unit - unit of the meter data(kwh)
# meter_id - an id for the meter
# meter_name - a name for identification
# renteknik_meter - an id for our identification
class ArcCreateMeter(BaseModel):
    leed_id: str
    client_name: str
    meter_type: int
    meter_unit: str
    meter_id: str
    meter_name: str
    renteknik_meter: str


    class Config:
        orm_mode = True



# Table for storing data from Z3
# cmd: data type
# time: measurement time
# ybase: year base, arg_hdr:, arg_m:
# data = [] - actual data
class z3_netmeter(BaseModel):
    cmd: str
    time: str
    ybase: str
    arg_hdr: str
    arg_m: str
    data: list
