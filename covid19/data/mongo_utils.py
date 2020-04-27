# -*- coding: utf-8 -*-
"""
@created on: 4/25/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""
import json
from covid19 import database

country_demog = database['country_demographics']


def fetch_from_collection(collection_name):
    return database[collection_name].find({})


def update_country_demog(update):
    country_demog.update({"_id": update['_id']}, {"$set": update}, upsert=True)


def download_country_demog(cname, save_path):
    json_arr = []
    data = database[cname].find({})
    for doc in data:
        for religion_name in doc['religion']:
            doc[f'religion_{religion_name}'] = doc['religion'][religion_name]
        doc.pop('_id')
        doc.pop('religion')
        json_arr.append(doc)
    json.dump(json_arr, open(save_path, 'w'), indent=4)


def download_county_demog(cname, save_path):
    json_arr = []
    data = database[cname].find({})
    for doc in data:
        doc.pop('_id')
        json_arr.append(doc)
    json.dump(json_arr, open(save_path, 'w'), indent=4)


download_country_demog('country_demographics', '/Users/badgod/badgod_documents/Datasets/covid19/country_demog.json')
download_county_demog('county_demographics', '/Users/badgod/badgod_documents/Datasets/covid19/county_demog.json')
