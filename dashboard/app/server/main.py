from fastapi import FastAPI
from covid19 import database as db
from fastapi.middleware.cors import CORSMiddleware
import json
from covid19 import COUNTIES, ETHNICITIES, COVID19_DATA_PATH
import random


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/county")
def get_county():
    # counties=[]
    # coll = db.get_collection("county_demographics")
    # for coll in coll.find({"country":"US"}):
    #     counties.append(coll["combined_key"].replace("|", ", "))
    # with open('/Users/prathyushsp/Git/covid19_research/covid19/data/COUNTIES.json', 'w') as f:
    #     json.dump(counties, f, indent=2)
    return {'data':COUNTIES}



@app.get("/v1/ethnicity")
def get_ethnicity():
    # counties=[]
    # coll = db.get_collection("county_demographics")
    # for coll in coll.find({"country":"US"}):
    #     counties.append(coll["combined_key"].replace("|", ", "))
    # with open('/Users/prathyushsp/Git/covid19_research/covid19/data/COUNTIES.json', 'w') as f:
    #     json.dump(counties, f, indent=2)
    return {'data':ETHNICITIES}


@app.get("/v1/modelVariables")
def get_variables():
    return {'data':[[e[:5],random.uniform(0, 1)] for e in ETHNICITIES]}

@app.get("/v1/stocks")
def get_stocks():
    return {'data':json.load(open(COVID19_DATA_PATH+'/'+'stocks.json'))}

@app.get("/v1/global_confirmed")
def get_stocks():
    return {'data':json.load(open(COVID19_DATA_PATH+'/'+'world_count.json'))}