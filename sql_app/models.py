from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from datetime import datetime

# Data base table structure for Panpower meta data
class PanpowerMetaData(Base):
    __tablename__ = "PanpowerMetaData"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String)
    client_name = Column(String)
    site_uid = Column(String)
    electrical_hierarchy = Column(String)
    timezone = Column(String)
    dst = Column(String)
    api_name = Column(String)
    device_sensor_types = Column(String)
    remarks = Column(String)


# Database table structure for panpowerpulsemeasurement
class PanpowerPulseMeasurement(Base):
    __tablename__ = "panpowerpulsemeasurements"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String)
    meter_id = Column(Integer)
    meter_type = Column(String)
    meter_name = Column(String)
    meter_unit = Column(String)
    measurement_time = Column(DateTime)
    resolution = Column(Integer)
    site_id = Column(Integer)
    site_name = Column(String)
    power = Column(Float)
    energy = Column(Float)
    energy_k = Column(Float)
    energy_m = Column(Float)
    flow = Column(Float)
    volume = Column(Float)



# Database table structure for panpower1012emeasurement
class Panpower1012Measurement(Base):
    __tablename__ = "panpower1012measurements"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String)
    device_id = Column(Integer)
    device_name = Column(String)
    measurement_time = Column(DateTime)
    resolution = Column(Integer)
    site_id = Column(Integer)
    site_name = Column(String)
    current = Column(Float)
    voltage = Column(Float)
    power = Column(Float)
    power_factor = Column(Float)
    energy = Column(Float)



# Database table structure for panpower42measurement
class Panpower42Measurement(Base):
    __tablename__ = "panpower42measurements"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String)
    device_id = Column(Integer)
    device_name = Column(String)
    measurement_time = Column(DateTime)
    resolution = Column(Integer)
    site_id = Column(Integer)
    site_name = Column(String)
    phase = Column(String)
    current = Column(Float)
    voltage = Column(Float)
    power = Column(Float)
    power_factor = Column(Float)
    energy = Column(Float)
    reactive_power = Column(Float)
    consumed_active_energy = Column(Float)
    frequency = Column(Float)


# Data base table structure for Arc metadata
class ArcMetaData(Base):
    __tablename__ = "ArcMetaData"

    id = Column(Integer, primary_key=True, index=True)
    leed_id = Column(String)
    client_name = Column(String)
    customer_name = Column(String)
    customer_uid = Column(String)
    timezone = Column(String)
    duration_format = Column(String)
    duration = Column(String)


# Database table for Arc Keys
class ArcKeyTable(Base):
    __tablename__ = "ArcKeyTable"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    current_time = Column(String)


# Database table for Arc meter details
class ArcMeterTable(Base):
    __tablename__ = "ArcMeterTable"

    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(String)
    leed_id = Column(String)
    customer_id = Column(String)
    meter_name = Column(String)
    meter_type = Column(String)
    meter_unit = Column(String)
    renteknik_meter = Column(String)
    duration_format = Column(String)
    duration = Column(String)
