# -*- coding: utf-8 -*-
"""
@created on: 4/18/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""
import json

import pandas as pd
import numpy as np
import requests
import time
from covid19 import database


class JHUTimeSeries:
    COUNTRIES_LOOKUP = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"
    CONFIRMED_US = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    CONFIRMED_GLOBAL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    DEATHS_US = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
    DEATHS_GLOBAL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    RECOVERED_GLOBAL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    COUNTY_LEVEL_INFOGRAPHICS = lambda \
            fips: f"https://services9.arcgis.com/6Hv9AANartyT7fJW/ArcGIS/rest/services/USCounties_cases_V1/FeatureServer/0/query?f=json&where=FIPS%3D%27{fips}%27&returnGeometry=false&outFields=*"


def push_json_arr(collection, json_arr):
    for doc in json_arr:
        collection.insert_one(doc)


def download_csv(url):
    try:
        df = pd.read_csv(url, error_bad_lines=False)
        if df is None or len(df) == 0:
            raise Exception("CSV downloaded from the URL is empty")
        return df
    except Exception as e:
        print(e)


def get_schema():
    return {"Country_Region": "", "Province_State": "", "datetime": "", "Confirmed": 0, "Recovered": 0,
            "Death": 0}


def create_unique_key(global_df, primary_key):
    global_df = global_df.fillna('')
    global_df[primary_key] = global_df['Country/Region'] + '_' + global_df['Province/State']
    return global_df


def access_df_cell(df, idx, colname):
    if idx in df.index:
        val = df.at[idx, colname]
        if pd.isnull(val) or val == '':
            return 0
        return int(val)
    else:
        return 0


def fetch_fips_county_level():
    def pop_from_dict(keys, dictionary):
        for key in keys:
            if key in dictionary:
                dictionary.pop(key)
        return dictionary

    infographics = []
    print('Downloading countries CSV...')
    countries_lookup = download_csv(JHUTimeSeries.COUNTRIES_LOOKUP)
    countries_lookup.fillna('', inplace=True)
    country_fips = [int(x) for x in countries_lookup['FIPS'].values if x != '']
    for i, fips in enumerate(country_fips):
        url = JHUTimeSeries.COUNTY_LEVEL_INFOGRAPHICS(fips)
        print('Fetching ', i, '/', len(country_fips))
        data = requests.get(url).json()
        if 'features' in data and len(data['features']) != 0:
            features = data['features'][0]['attributes']
            to_pop = ['OBJECTID', 'Countyname', 'Thumbnail']
            features = pop_from_dict(to_pop, features)
            infographics.append(features)
    print(infographics)
    json.dump(infographics, open('county_infographics_updated.json', 'w'), indent=4)


if __name__ == '__main__':
    # fetch_fips_county_level()
    # exit()
    pd.set_option('display.max_columns', None)

    # COUNTRY AND COUNTY LEVEL META DATA
    print('Downloading countries CSV...')
    countries_lookup = download_csv(JHUTimeSeries.COUNTRIES_LOOKUP)
    countries_lookup.set_index('Combined_Key', inplace=True)

    country_level_document = countries_lookup[countries_lookup['Province_State'].isnull()]
    country_level_document = country_level_document.fillna('')

    county_document = countries_lookup[~countries_lookup['Province_State'].isnull()]
    county_document = county_document.fillna('')
    county_document['FIPS'] = county_document['FIPS'].astype(str)
    county_document['FIPS'] = county_document['FIPS'].apply(lambda x: x.split(".")[0])

    # CONFIRMED DEATH ACTIVE RECOVERED STATUS
    status_documents = []

    primary_join_key = 'primary_key'
    print('Downloading confirmed global file...')
    confirmed_global = download_csv(JHUTimeSeries.CONFIRMED_GLOBAL)
    timestamps_global = list(confirmed_global.columns)[4:]
    confirmed_global = create_unique_key(confirmed_global, primary_join_key)

    print('Downloading deaths global file...')
    deaths_global = download_csv(JHUTimeSeries.DEATHS_GLOBAL)
    deaths_global = create_unique_key(deaths_global, primary_join_key)

    print('Downloading recovered global file...')
    recovered_global = download_csv(JHUTimeSeries.RECOVERED_GLOBAL)
    recovered_global = create_unique_key(recovered_global, primary_join_key)

    start = time.time()

    confirmed_global.set_index(primary_join_key, inplace=True)
    deaths_global.set_index(primary_join_key, inplace=True)
    recovered_global.set_index(primary_join_key, inplace=True)
    print('Creating "CONFIRMED, DEATH, ACTIVE, RECOVERED" status by country and province...')

    for idx, row in confirmed_global.iterrows():
        for i, datetime in enumerate(timestamps_global):
            schema = get_schema()
            schema['datetime'] = datetime
            schema['Confirmed'] = row[datetime]
            schema['Death'] = access_df_cell(deaths_global, idx, datetime)
            schema['Recovered'] = access_df_cell(recovered_global, idx, datetime)
            schema['Country_Region'] = row['Country/Region']
            schema['Province_State'] = row['Province/State']
            schema['County'] = ''
            status_documents.append(schema)
    print('Processing of global data done...')

    print('Downloading confirmed US file...')
    confirmed_us = download_csv(JHUTimeSeries.CONFIRMED_US)
    print('Downloading deaths US file...')
    deaths_us = download_csv(JHUTimeSeries.DEATHS_US)
    primary_join_key = 'Combined_Key'
    timestamps_us = confirmed_us.columns[11:]

    """
     Notes: No recovered data is given county wise.
    """
    confirmed_us.fillna('', inplace=True)
    confirmed_us.set_index(primary_join_key, inplace=True)
    deaths_us.set_index(primary_join_key, inplace=True)
    print('Iterating over US data...')
    for idx, row in confirmed_us.iterrows():
        state = row['Province_State']
        country = row['Country_Region']
        county = row['Admin2']
        fips = access_df_cell(countries_lookup, idx, 'FIPS')
        for i, datetime in enumerate(timestamps_us):
            schema = get_schema()
            schema['datetime'] = datetime
            schema['Confirmed'] = row[datetime]
            schema['Death'] = access_df_cell(deaths_us, idx, datetime)
            schema['Country_Region'] = country
            schema['Province_State'] = state
            schema['County'] = county
            schema['fips'] = fips
            status_documents.append(schema)
    print('US data processed...')


    country_level_document = country_level_document.to_dict(orient='record')
    county_document = county_document.to_dict(orient='record')
    json.dump(country_level_document, open('country_level_documents.json', 'w'), indent=4)
    json.dump(county_document, open('county_level_documents.json', 'w'), indent=4)
    json.dump(status_documents, open('status_documents.json', 'w'), indent=4)

    # collection = database.get_collection("country_level_metadata")
    # push_json_arr(collection, country_level_document)
    #
    # collection = database.get_collection("state_level_metadata")
    # push_json_arr(collection, county_document)
    #
    # collection = database.get_collection("world_status")
    # push_json_arr(collection, status_documents)
