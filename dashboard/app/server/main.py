from fastapi import FastAPI
from covid19 import database as db
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/v1/counties")
def get_counties():
    counties=[]
    coll = db.get_collection("county_demographics")
    for coll in coll.find({"country":"US"}):
        counties.append(coll["combined_key"])
    return {"counties": counties}

