# CRUD: CREATE READ UPDATE DELETE


from sqlalchemy.orm import Session

from . import models, schemas



# Add the provided values to the Pan42 table.
def create_pan42(db: Session, measurements: schemas.Pan42DictCover):
    measurements = measurements.dict()
    for measurement in measurements:
        measure = measurements[measurement]
        for val in measure:
            # print(f"val = {val}")
            db_measurement = models.Panpower42Measurement(**val)
            db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the panpower pulse table.
def create_panpulse(db: Session, measurements: schemas.PanpowerPulseDictCover):
    measurements = measurements.dict()
    for measurement in measurements:
        measure = measurements[measurement]
        for val in measure:
            # print(f"val = {val}")
            db_measurement = models.PanpowerPulseMeasurement(**val)
            db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the panpower 10/12 table.
def create_panpower(db: Session, measurements: schemas.PanPowerDictCover):
    measurements = measurements.dict()
    for measurement in measurements:
        measure = measurements[measurement]
        for val in measure:
            print(f"val = {val},\n")
            db_measurement = models.Panpower1012Measurement(**val)
            db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the arc meta data table
def create_arc_metadata(db: Session, arc_meta_data: schemas.ArcMetaData):
    arc_meta_data = arc_meta_data.dict()
    print(arc_meta_data)
    db_measurement = models.ArcMetaData(**arc_meta_data)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Get the given client name from panpower1012
def get_panpower1012_client(db: Session, client_name: str):
    return db.query(models.Panpower1012Measurement).filter(models.Panpower1012Measurement.client == client_name).first()


# Get data from panpower1012 based on client name
def get_panpower1012_client_data(db: Session, client_name: str):
    return db.query(models.Panpower1012Measurement).filter(models.Panpower1012Measurement.client == client_name).all()


# Get the given client name from pan42
def get_pan42_client(db: Session, client_name: str):
    return db.query(models.Panpower42Measurement).filter(models.Panpower42Measurement.client == client_name).first()


# Get data from pan42 based on client name
def get_pan42_client_data(db: Session, client_name: str):
    return db.query(models.Panpower42Measurement).filter(models.Panpower42Measurement.client == client_name).all()


# Get the given client name from pan42
def get_panpowerpulse_client(db: Session, client_name: str):
    return db.query(models.PanpowerPulseMeasurement).filter(models.PanpowerPulseMeasurement.client == client_name).first()


# Get data from panpower pulse based on client name
def get_panpowerpulse_client_data(db: Session, client_name: str):
    return db.query(models.PanpowerPulseMeasurement).filter(models.PanpowerPulseMeasurement.client == client_name).all()


# Get the given client name from panpower1012
def get_arc_meterdata(db: Session, meter_id: str):
    return db.query(models.ArcMetaData).filter(models.ArcMetaData.meter_id == meter_id).first()


# Get the given client name from panpower1012
def get_arc_metadata(db: Session, client_name: str):
    return db.query(models.ArcMetaData).filter(models.ArcMetaData.client_id == client_name).all()
