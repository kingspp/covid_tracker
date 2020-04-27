from fastapi import FastAPI
from covid19 import database as db

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/counties")
def read_item():
    counties=[]
    coll = db.get_collection("county_demographics")
    for coll in coll.find({"country":"US"}):
        counties.append(coll["combined_key"])
    return {"counties": counties}

read_item()