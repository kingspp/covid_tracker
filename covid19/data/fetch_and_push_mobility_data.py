# Country Median Data
import json
from covid19 import COVID19_DATA_PATH, COUNTRIES, database
from covid19.data import GoogleMobilityRecords
import pandas as pd
import requests
from covid19.utils import JsonEncoder

response = requests.get("https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv")
with open(COVID19_DATA_PATH+"/google_mobility_data_latest.csv", 'w') as f:
    f.write(response.text)


GMR_COUNTRY_MAPPER = json.load(open(COVID19_DATA_PATH+"/google_mobility_data_country_mapper.json"))
SKIP_COUNTRIES = ["Tajikistan", "Zimbabwe", "RÃ©union", "Puerto Rico", "Hong Kong", "Cape Verde","Aruba"]
df = pd.read_csv(COVID19_DATA_PATH+"/google_mobility_data_latest.csv")

df.dropna(inplace=True,subset=["retail_and_recreation_percent_change_from_baseline",
                               "grocery_and_pharmacy_percent_change_from_baseline",
                               "parks_percent_change_from_baseline",
                               "transit_stations_percent_change_from_baseline",
                               "workplaces_percent_change_from_baseline",
                               "residential_percent_change_from_baseline"])

print("====" * 20)
print("Countries not found in gmr data . . .")
for country in df['country_region']:
    if country not in COUNTRIES:
        if country not in GMR_COUNTRY_MAPPER :
            if country not in SKIP_COUNTRIES:
                print(country)



gmr = GoogleMobilityRecords()

gmr_collection = []

# GMR Collection
for row in df.iterrows():
    row = row[1].to_dict()
    country = row["country_region"]
    if country in SKIP_COUNTRIES:
        continue
    country =  country if country in COUNTRIES else GMR_COUNTRY_MAPPER[country]
    gmr_collection.append(GoogleMobilityRecords(country_code=row['country_region_code'],
                                         country=country,
                                         sub_region_1=row["sub_region_1"],
                                         sub_region_2=row['sub_region_2'],
                                         date=row["date"],
                                         retail_and_recreation_percent_change_from_baseline=row["retail_and_recreation_percent_change_from_baseline"],
                                         grocery_and_pharmacy_percent_change_from_baseline=row["grocery_and_pharmacy_percent_change_from_baseline"],
                                         parks_percent_change_from_baseline=row["parks_percent_change_from_baseline"],
                                         transit_stations_percent_change_from_baseline=row["transit_stations_percent_change_from_baseline"],
                                         workplaces_percent_change_from_baseline=row["workplaces_percent_change_from_baseline"],
                                         residential_percent_change_from_baseline=row["residential_percent_change_from_baseline"],
                                         ))


def insert():
    # Insert Mobility Records Collection
    database.drop_collection("gmr_collection")
    collection = database.get_collection("gmr_collection")
    for coll in gmr_collection:
        collection.insert(coll.__dict__)

insert()