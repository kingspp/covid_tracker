# Country Median Data
import json
from covid19.data import CountryDemographics, ContinentDemographics, WorldDemographics, Religion, CountyDemographics
from covid19 import COVID19_DATA_PATH, COUNTRIES
import pandas as pd
from collections import defaultdict

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

print("====" * 20)
print("Countries not Lockdown . . .")
country_lockdown = pd.read_csv(COVID19_DATA_PATH + "/Lockdown_Dates.csv", header=0)
lockdown_countries = country_lockdown["Country"].values.tolist()
for country in lockdown_countries:
    if country not in COUNTRIES:
        print(country)

print("====" * 20)
print("Countries not Masks . . .")
masks_data = pd.read_csv(COVID19_DATA_PATH + "/masks.csv", header=0)
mask_countries = masks_data["Country"].values.tolist()
for country in mask_countries:
    if country not in COUNTRIES:
        print(country)

def check_number(num_str):
    num_str = num_str.replace(",", "")
    num_str = num_str.replace(">", "")
    num_str = num_str.replace("<", "")
    return num_str

# County Metrics
county_demog_data = json.load(open(COVID19_DATA_PATH+"county_level_documents.json"))
county_collection = []

county_infographics = json.load(open(COVID19_DATA_PATH+"infographics.json"))
county_infographics = {county['FIPS']:county for county in county_infographics}

for county in county_demog_data:
    if county["FIPS"]!="" and county["FIPS"] in county_infographics:
        infographics = county_infographics[county["FIPS"]]
    else:
        infographics =defaultdict(lambda:"")
    if county["Admin2"]in ["", "Unassigned", ""] or 'Out of' in county["Admin2"] :
        continue
    county_collection.append(CountyDemographics(country=county["Country_Region"],state=county["Province_State"],
                                                uid=county["UID"], iso2=county["iso2"], iso3=county["iso3"],
                                                code3=county["code3"], fips=county["FIPS"], county=county["Admin2"],
                                                latitude=county["Lat"], longitude=county["Long_"],
                                                jhu_county_population=county["Population"],
                                                infographics_population= infographics["POP_ESTIMA"],
                                                poverty_percent_state=infographics["PCTPOVALL_"],
                                                infographics_date=infographics["DateChecke"],
                                                unemployment_rate=infographics["Unemployme"],
                                                total_unemployed=infographics["Unemployed"],
                                                median_household_income_perc_of_state = infographics["Med_HH_Inc"],
                                                median_household_income = infographics["Median_Hou"],
                                                emergency_declaration_date=infographics["EM_date"],
                                                emergency_declation_type=infographics["EM_type"],
                                                emergency_declaration_notes=infographics["EM_notes"],
                                                url=infographics["url"],
                                                staffed_beds=infographics["Beds_Staff"],
                                                licenced_beds=infographics["Beds_Licen"],
                                                icu_beds=infographics["Beds_ICU"],
                                                average_ventilator_used_per_hospital=infographics["Ventilator"],
                                                poverty_rate=infographics["POVALL_201"],
                                                combined_key='|'.join([county["Admin2"],county["Province_State"],county["Country_Region"]])
                                                ))


# Country Metrics
country_demog_data = json.load(open(COVID19_DATA_PATH+"country_level_documents.json"))
country_demog_data = {country["Country_Region"]:country for country in country_demog_data}

for country in COUNTRIES:
    if country in median_age and country in rel_available_countries:
        lockdown_start_date = country_lockdown.loc[country_lockdown['Country'] == country]["Start Date"].values[0] if country in lockdown_countries else ""
        lockdown_end_date = country_lockdown.loc[country_lockdown['Country'] == country]["End Date"].values[0] if country in lockdown_countries else ""
        rel = country_religion.loc[country_religion["Country"] == country]
        religion = Religion( christians=float(check_number(rel['Christians'].values[0])),
                                                        buddhists=float(check_number(rel['Buddhists'].values[0])),
                                                        hindus=float(check_number(rel['Hindus'].values[0])),
                                                        muslims=float(check_number(rel['Muslims'].values[0])),
                                                        unaffiliated=float(check_number(rel['Unaffiliated'].values[0])),
                                                        folk_religions=float(
                                                            check_number(rel['Folk Religions'].values[0])),
                                                        other_religions=float(
                                                            check_number(rel['Other Religions'].values[0])),
                                                        jews=float(check_number(rel['Jews'].values[0])))
        country_demographics.append(CountryDemographics(country=country,
                                                        country_median_age=median_age[country],
                                                        religion=religion.__dict__,
                                                        continent=rel["Region"].values[0],
                                                        country_government_type=country_gov[country],
                                                        uid=country_demog_data[country]["UID"],
                                                        latitude=country_demog_data[country]["Lat"],
                                                        longitude=country_demog_data[country]["Long_"],
                                                        iso2=country_demog_data[country]["iso2"],
                                                        iso3=country_demog_data[country]["iso3"],
                                                        code3=country_demog_data[country]["code3"],
                                                        fips=country_demog_data[country]["FIPS"],
                                                        county=country_demog_data[country]["Admin2"],
                                                        state=country_demog_data[country]["Province_State"],
                                                        jhu_country_population=country_demog_data[country]["Population"],
                                                        lockdown_start_date=lockdown_start_date,
                                                        lockdown_end_date=lockdown_end_date
                                                        ))

number_of_countries = country_religion.groupby("Region").count()['Country'].to_dict()
world_religion_data = \
    country_religion.loc[
        (country_religion['Country'] == "All Countries") & (country_religion['Region'] == "World")].iloc[
        0].to_dict()


# Continent Metrics
for continent in country_religion.loc[
    (country_religion['Country'] == "All Countries") & (country_religion['Region'] != "World")].iterrows():
    continent = continent[1]
    continent_name = continent['Region']
    religion = Religion(christians=float(check_number(continent['Christians'])),
                                                        buddhists=float(check_number(continent['Buddhists'])),
                                                        hindus=float(check_number(continent['Hindus'])),
                                                        muslims=float(check_number(continent['Muslims'])),
                                                        unaffiliated=float(check_number(continent['Unaffiliated'])),
                                                        folk_religions=float(
                                                            check_number(continent['Folk Religions'])),
                                                        other_religions=float(
                                                            check_number(continent['Other Religions'])),
                                                        jews=float(check_number(continent['Jews'])))
    continent_demographics.append(ContinentDemographics(continent=continent_name,
                                                        number_of_countries=number_of_countries[continent_name],
                                                        religion=religion.__dict__
                                                        ))

# World Metrics
religion = Religion(christians=float(check_number(world_religion_data['Christians'])),
                                       buddhists=float(check_number(world_religion_data['Buddhists'])),
                                       hindus=float(check_number(world_religion_data['Hindus'])),
                                       muslims=float(check_number(world_religion_data['Muslims'])),
                                       unaffiliated=float(check_number(world_religion_data['Unaffiliated'])),
                                       folk_religions=float(check_number(world_religion_data['Folk Religions'])),
                                       other_religions=float(check_number(world_religion_data['Other Religions'])),
                                       jews=float(check_number(world_religion_data['Jews'])))
world_demographics = WorldDemographics(number_of_continents=6, number_of_countries=sum((number_of_countries.values())),
                                       world_population=float(check_number(world_religion_data['All Religions'])),
                                       religion=religion.__dict__
                                       )


# print(json.dumps(country_demographics[0], indent=2, cls=JsonEncoder))
# print(json.dumps(continent_demographics[0], indent=2, cls=JsonEncoder))
# print(json.dumps(world_demographics, indent=2, cls=JsonEncoder))


def insert():
    from covid19 import database

    # Insert County Demographics
    database.drop_collection("county_demographics")
    collection = database.get_collection("county_demographics")
    for county in county_collection:
        collection.insert(county.__dict__)

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