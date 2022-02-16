#!/usr/bin/env python3

from datetime import datetime
from fastapi import  HTTPException
from sql_app import models, schemas, crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
import sys
from pytz import timezone, UTC

sys.path.append('/abacus/sql_app')

models.Base.metadata.create_all(bind=engine)

# Now use the SessionLocal class we created in the sql_app/databases.py file to create a dependency
# We need to  have an independent database connection per request
# use the same session through all the request and then close it after the request is finished
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to change one time zone to another
# inputs: date to be changed: in date time format
# zone name: The zone to which the given date should be converted
def change_timezone(date: datetime, zonename: str):
    # out put format of changed timezone
    fmt = "%Y-%m-%dT%H:%M:%S"

    # assigning input date as UTC time format
    input_zone = timezone('UTC')

    # change input date to changed time zone
    zone = timezone(zonename)
    input_datetime = input_zone.localize(date, is_dst=True)
    changed_datetime = zone.localize(date, is_dst=True)
    changed_datetime = input_datetime.astimezone(zone)

    # change returning timezone changed date to required format
    changed_datetime = changed_datetime.strftime(fmt)
    return_date = datetime.strptime(changed_datetime, fmt)
    return return_date



# date validate function
def validate_dates(date1: str, date2: str):

    # Time format
    fmt = "%Y-%m-%d"

    # Removing the extra z from the panpower data
    # Inorder to make the date format compatible with Arc
    if date1.endswith('Z'):
        date1 = date1[:-1]

    is_valid_date = True

    try:
        date1 = datetime.strptime(date1, fmt)
        date2 = datetime.strptime(date2, fmt)
    except ValueError:
        is_valid_date = False

    return [is_valid_date, date1, date2]



# validate start and end dates are in order
# Start date should be earlier than end date
def validate_start_end_dates(date1: datetime, date2: datetime):

    difference = (date2 - date1).days

    valid_start_end_date = False

    if difference > 0:

        valid_start_end_date = True

    return valid_start_end_date


# Add energy for energy star
def sum_of_energy(datain: schemas.PanPowerDictCover):
    sum_energy = 0
    for value in datain:
        print(value.measurement_time, "\t", value.energy, "\t",  value.device_name)
        sum_energy = sum_energy + value.energy
    return sum_energy/1000


# calculating flow for 1-3 reandrive specifically
def sum_of_flow_reandrive(datain: schemas.PanpowerPulse, start_date: datetime, end_date: datetime):
    water_volume = 0
    hot_water_volume = 0
    gas_meter = 0
    result = {}
    duration = (end_date - start_date).days
    for value in datain:
        print(value.measurement_time, value.meter_name, value.volume)
        if (value.meter_name == "Spa water meter") or (value.meter_name == "Pool Water") or (value.meter_name == "Cold Water"):
            water_volume = water_volume + value.volume
        elif value.meter_name == "Hot Water":
            hot_water_volume = hot_water_volume + value.volume
        elif value.meter_name == "GAS METER":
            gas_meter = gas_meter + value.volume
        else:
            print("different parameter")

    hot_water_volume = hot_water_volume - (100*24*duration)
    print(water_volume, hot_water_volume, gas_meter)
    result = {"water_volume": water_volume, "hot_water_volume": hot_water_volume, "gas_meter": gas_meter}

    return result

# Add flow value from pulse data
def sum_of_flow(datain: schemas.PanpowerPulse, start_date: datetime, end_date: datetime):
    if datain[0].client == "1-3reandrive":
        result = sum_of_flow_reandrive(datain, start_date, end_date)
    return result


# energy star report generation - Initial validation funtion
def energy_star_report(db: Session, data: str, client: str, start_date: str, end_date: str):

    #Validate whether the input strings are actual dates
    is_valid_date = validate_dates(start_date, end_date)
    sum_energy = 0

    if is_valid_date[0]:

        # if they are valid dates, check whether they are in order
        # ie start date lesser than end date
        valid_start_end_date = validate_start_end_dates(is_valid_date[1], is_valid_date[2])

        if valid_start_end_date:

            # if they are in order set the dates in order flag
            start_date = is_valid_date[1]
            end_date = is_valid_date[2]
            date_in_order = True
        else:
            # date not in order
            date_in_order = False
            raise HTTPException(status_code=404, detail="Dates not in order")


    else:
        # Dates not valid
        raise HTTPException(status_code=404, detail="Dates not valid")


    if date_in_order:

        # print("dates in order")
        if data == "panpower1012":
            db_client = crud.energy_star_fetch_data(db=db, client=client, start_date=start_date, end_date=end_date)

            if db_client == 0:
                raise HTTPException(status_code=404, detail="Client not found")


            sum_energy = sum_of_energy(db_client)
            # return sum_energy, db_client[0].measurement_time, db_client[len(db_client) - 1].measurement_time
            return sum_energy

        elif data == "panpowerpulse":
            db_client = crud.energy_star_fetch_pulsedata(db=db, client=client, start_date=start_date, end_date=end_date)

            if db_client == 0:
                raise HTTPException(status_code=404, detail="Client not found")

            else:
                sum_flow = sum_of_flow(db_client, start_date, end_date)
                return sum_flow

           
    else:
        print("dates not in order")
        raise HTTPException(status_code=404, detail="Dates not in order")



    # return data, client, start_date, end_date
