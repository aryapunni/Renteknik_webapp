
from fastapi import FastAPI
import sqlalchemy

app = FastAPI()


panpower = {}


# panpower post function
@app.post("/panpower")
async def post_panpower(datain: dict):
    global panpower
    panpower = datain
    return 1


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
