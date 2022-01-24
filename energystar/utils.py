#!/usr/bin/env python3

from datetime import datetime
from fastapi import  HTTPException
from sql_app import models, schemas, crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
import sys

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
        sum_energy = sum_energy + value.energy
    return sum_energy


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
        print("dates not in order")
        raise HTTPException(status_code=404, detail="Dates not in order")



    # return data, client, start_date, end_date
