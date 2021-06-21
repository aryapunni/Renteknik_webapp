from typing import Optional, List, Union
from pydantic import BaseModel, Field, ValidationError, validator, root_validator


# function to find whether input in float or string
# if float: o/p = 1, if string: o/p = 0
def float_or_string(value):
    if isinstance(value, float):
        return 1
    elif isinstance(value, str):
        return 0


# Schema for panpower pulse measurements
class PanpowerPulse(BaseModel):
    client: Optional[str]
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


# schema for array of measurements(panpower pulse)
class PanpowerPulseDictCover(BaseModel):
    measurements: List[PanpowerPulse]


# Base class for panpower(Testing)
class PanPower(BaseModel):
    client: Optional[str]
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

    class Config:
        orm_mode = True


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
    meter_id: Optional[str]
    measurement_time: str = Field(..., alias='measurement_time(UTC)')
    energy: float = Field(..., alias='energy(Wh)')


# schema for arc data CO2
class ArcCo2Consumption(BaseModel):
    client: str
    meter_id: str
    leed_id: str
    meter_id: int = Field(..., alias='METER_ID')
    measurement_time: str = Field(..., alias='measurement_time(UTC)')
    energy: float = Field(..., alias='energy(Wh)')



# schema for ArcEnergyConsumption
class ArcEnergyDictCover(BaseModel):
    measurements: List[ArcEnergyConsumption]



# class TestOne(BaseModel):
#     device_id: int
#     measurement: float


# class TestMulti(BaseModel):
#     measurements: List[TestOne]

# if __name__ == "__main__":
#     test1 = TestOne(device_id=5, measurement=3.15)
#     test_multi = TestMulti(measurements=[test1])
#     print(test_multi.dict())
