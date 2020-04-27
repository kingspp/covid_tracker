# -*- coding: utf-8 -*-
"""
@created on: 4/24/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""

import json

import pandas as pd
from covid19.data.mongo_utils import fetch_from_collection, update_country_demog
from covid19 import COVID19_DATA_PATH

population_df = pd.read_csv(COVID19_DATA_PATH + '/TotalPopulationBySex_2020.csv')
population_df.set_index('Location', inplace=True)
population_df = population_df.drop(['LocID', 'Time', 'MidPeriod', 'VarID', 'Variant'], axis=1)

COUNTRY_MAPPER = json.load(open(COVID19_DATA_PATH + "/UN_country_mapper.json"))

docs = fetch_from_collection('country_demographics')
for doc in docs:
    update = {}
    country = doc['country']

    # For country names which have conflict - fetch from db, get the alias from json. Using the alias fetch
    # information from DataFrame(UN population). Update this information back to db for the corresponding country
    country = COUNTRY_MAPPER[country] if country in COUNTRY_MAPPER.keys() else country
    if country in population_df.index:
        print(f'Updating {country}')
        d = population_df.loc[country]
        update['_id'] = doc['_id']
        update['country_male_population'] = d['PopMale'] * 1000
        update['country_female_population'] = d['PopFemale'] * 1000
        update['country_population'] = d['PopTotal'] * 1000
        update['country_population_density'] = d['PopDensity']
        update_country_demog(update)
    else:
        print(f'Data not found for {country}')
        continue
