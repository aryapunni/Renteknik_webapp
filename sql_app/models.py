from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


# Database table structure for panpowerpulsemeasurement
class PanpowerPulseMeasurement(Base):
    __tablename__ = "panpowerpulsemeasurements"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String)
    meter_id = Column(Integer)
    meter_type = Column(String)
    meter_name = Column(String)
    meter_unit = Column(String)
    measurement_time = Column(String)
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
    measurement_time = Column(String)
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
    measurement_time = Column(String)
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
