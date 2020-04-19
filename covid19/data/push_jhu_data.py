import json
from covid19 import COVID19_DATA_PATH
from covid19.utils import JsonEncoder
from covid19.data import Statistics


statistics_collection = []
statistics = json.load(open(COVID19_DATA_PATH+"status_documents.json"))
county_data = json.load(open(COVID19_DATA_PATH+"county_level_documents.json"))
county_data = {f'{county["Country_Region"]}_{county["Province_State"]}_{county["Admin2"]}':county for county in county_data}

del_confirmed, del_recovered, del_death, del_active = 0, 0, 0, 0
country = statistics[0]["Country_Region"]
for rec in statistics:
    if (rec["Country_Region"] != country):
        del_confirmed, del_recovered, del_death, del_active = 0, 0, 0, 0
        country = rec["Country_Region"]

    active = rec["Confirmed"]-rec["Recovered"]-rec["Death"]
    ckey = rec["Country_Region"]+"_"+rec["Province_State"]+"_"+rec["County"]
    population = int(county_data[ckey]['Population']) if ckey in county_data and county_data[ckey]['Population']!="" else 0
    if population>0:
        confirmed_by_population =  rec["Confirmed"]/population
        deaths_by_population = rec["Death"]/population
        active_by_population = active/population
        recovered_by_population= rec["Recovered"]/population
    else:
        confirmed_by_population,deaths_by_population,active_by_population,recovered_by_population=0,0,0,0
    statistics_collection.append(Statistics(country=rec["Country_Region"],
                                            province=rec["Province_State"],
                                            date=rec["datetime"],
                                            confirmed=rec["Confirmed"],
                                            recovered=rec["Recovered"],
                                            death=rec["Death"],
                                            active=active,
                                            confirmed_delta=rec["Confirmed"]-del_confirmed,
                                            recovered_delta=rec["Recovered"]-del_recovered,
                                            death_delta=rec["Death"]-del_death,
                                            active_delta=active-del_active,
                                            recovery_rate=rec["Recovered"]/(rec["Confirmed"]+1e-5),
                                            death_rate = rec["Death"]/(rec["Confirmed"]+1e-5),
                                            active_rate=active / (rec["Confirmed"]+1e-5),
                                            county=rec["County"],
                                            confirmed_by_population=confirmed_by_population,
                                            deaths_by_population=deaths_by_population,
                                            recovered_by_population=recovered_by_population,
                                            active_by_population=active_by_population
                                            ))
    del_confirmed = rec["Confirmed"]
    del_recovered = rec["Recovered"]
    del_death = rec["Death"]
    del_active = active




print(json.dumps(statistics_collection[0], indent=2, cls=JsonEncoder))

def insert():
    from covid19 import database
    database.drop_collection("statistics")
    collection = database.get_collection("statistics")
    for coll in statistics_collection:
        collection.insert(coll.__dict__)

# insert()