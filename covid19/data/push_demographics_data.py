# Country Median Data
import json
from covid19.data import CountryDemographics, ContinentDemographics, WorldDemographics
from covid19 import COVID19_DATA_PATH, COUNTRIES
import pymongo
from covid19.utils import JsonEncoder
import pandas as pd

country_demographics = []
continent_demographics = []
world_demographics = []
print("====" * 20)
print("Countries not found in median age . . .")
median_age = json.load(open(COVID19_DATA_PATH + "median_age.json"))
for country in COUNTRIES:
    if country not in median_age:
        print(country)

print("====" * 20)
print("Countries not found in religion . . .")
country_religion = pd.read_csv(COVID19_DATA_PATH + "/Religious_Composition_by_Country_2020_v1.csv", header=0)
rel_available_countries = country_religion['Country'].values.tolist()
for country in COUNTRIES:
    if country not in rel_available_countries:
        print(country)

print("====" * 20)
print("Countries not found in government type . . .")
country_gov = pd.read_csv(COVID19_DATA_PATH + "/government_type.csv", header=0)
country_gov = dict(zip(country_gov["Country"], country_gov["GovernmentType"]))
gov_available_countries = list(country_gov.keys())
for country in COUNTRIES:
    if country not in gov_available_countries:
        print(country)

def check_number(num_str):
    num_str = num_str.replace(",", "")
    num_str = num_str.replace(">", "")
    num_str = num_str.replace("<", "")
    return num_str

for country in COUNTRIES:
    if country in median_age and country in rel_available_countries:
        rel = country_religion.loc[country_religion["Country"] == country]
        country_demographics.append(CountryDemographics(country=country,
                                                        country_median_age=median_age[country],
                                                        christians=float(check_number(rel['Christians'].values[0])),
                                                        buddhists=float(check_number(rel['Buddhists'].values[0])),
                                                        hindus=float(check_number(rel['Hindus'].values[0])),
                                                        muslims=float(check_number(rel['Muslims'].values[0])),
                                                        unaffiliated=float(check_number(rel['Unaffiliated'].values[0])),
                                                        folk_religions=float(
                                                            check_number(rel['Folk Religions'].values[0])),
                                                        other_religions=float(
                                                            check_number(rel['Other Religions'].values[0])),
                                                        jews=float(check_number(rel['Jews'].values[0])),
                                                        continent=rel["Region"].values[0],
                                                        country_government_type=country_gov[country]
                                                        ))

number_of_countries = country_religion.groupby("Region").count()['Country'].to_dict()
world_religion_data = \
    country_religion.loc[
        (country_religion['Country'] == "All Countries") & (country_religion['Region'] == "World")].iloc[
        0].to_dict()
# Update Continent Data
for continent in country_religion.loc[
    (country_religion['Country'] == "All Countries") & (country_religion['Region'] != "World")].iterrows():
    continent = continent[1]
    continent_name = continent['Region']
    continent_demographics.append(ContinentDemographics(continent=continent_name,
                                                        number_of_countries=number_of_countries[continent_name],
                                                        christians=float(check_number(continent['Christians'])),
                                                        buddhists=float(check_number(continent['Buddhists'])),
                                                        hindus=float(check_number(continent['Hindus'])),
                                                        muslims=float(check_number(continent['Muslims'])),
                                                        unaffiliated=float(check_number(continent['Unaffiliated'])),
                                                        folk_religions=float(
                                                            check_number(continent['Folk Religions'])),
                                                        other_religions=float(
                                                            check_number(continent['Other Religions'])),
                                                        jews=float(check_number(continent['Jews'])),
                                                        ))

world_demographics = WorldDemographics(number_of_continents=6, number_of_countries=sum((number_of_countries.values())),
                                       world_population=float(check_number(world_religion_data['All Religions'])),
                                       christians=float(check_number(world_religion_data['Christians'])),
                                       buddhists=float(check_number(world_religion_data['Buddhists'])),
                                       hindus=float(check_number(world_religion_data['Hindus'])),
                                       muslims=float(check_number(world_religion_data['Muslims'])),
                                       unaffiliated=float(check_number(world_religion_data['Unaffiliated'])),
                                       folk_religions=float(check_number(world_religion_data['Folk Religions'])),
                                       other_religions=float(check_number(world_religion_data['Other Religions'])),
                                       jews=float(check_number(world_religion_data['Jews'])),
                                       )


# print(json.dumps(country_demographics[0], indent=2, cls=JsonEncoder))
# print(json.dumps(continent_demographics[0], indent=2, cls=JsonEncoder))
# print(json.dumps(world_demographics, indent=2, cls=JsonEncoder))


def insert():
    # client = pymongo.MongoClient(host="192.168.1.16")
    # database = client.get_database("covid19_research")
    from covid19 import database

    # Insert Country Demographics
    database.drop_collection("country_demographics")
    collection = database.get_collection("country_demographics")
    for country in country_demographics:
        collection.insert(country.__dict__)

    # Insert Continent Demographics
    database.drop_collection("continent_demographics")
    collection = database.get_collection("continent_demographics")
    for continent in continent_demographics:
        collection.insert(continent.__dict__)

    # Insert World Demographics
    database.drop_collection("world_demographics")
    collection = database.get_collection("world_demographics")
    collection.insert(world_demographics.__dict__)

insert()