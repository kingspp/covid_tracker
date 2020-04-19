import json
from covid19 import COVID19_DATA_PATH
from covid19.utils import JsonEncoder
from covid19.data import Statistics


statistics_collection = []
statistics = json.load(open(COVID19_DATA_PATH+"status_documents.json"))

del_confirmed, del_recovered, del_death, del_active = 0, 0, 0, 0
country = statistics[0]["Country_Region"]
for rec in statistics:
    if (rec["Country_Region"] != country):
        del_confirmed, del_recovered, del_death, del_active = 0, 0, 0, 0
        country = rec["Country_Region"]

    active = rec["Confirmed"]-rec["Recovered"]-rec["Death"]
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
                                            active_delta=active-del_active))
    del_confirmed = rec["Confirmed"]
    del_recovered = rec["Recovered"]
    del_death = rec["Death"]
    del_active = active




print(json.dumps(statistics_collection[0], indent=2, cls=JsonEncoder))

def insert():
    from covid19 import database
    # Insert Nucleotide Collection
    database.drop_collection("ncbi_nucleotide")
    collection = database.get_collection("ncbi_nucleotide")
    for coll in statistics_collection:
        collection.insert(coll.__dict__)

insert()