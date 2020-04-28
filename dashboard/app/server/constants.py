# -*- coding: utf-8 -*-
"""
@created on: 4/27/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""


class ModelConstants:
    SAVE_PATH: str = "covid19/models/rf_model.pk"
    COUNTY_RANK_MAPPING_FILE: str = "covid19/data/county_ranking_map.json"
    COUNTY_PROCESSED_DATA: str = "covid19/data/processed_confirmed_cases_data_apr26th.csv"
    TIME_SERIES_LEN = 90
    COUNTY_ETHNICITY_AND_AGE_GRPS = "covid19/data/latest_ethnic_age_county_level_demog.csv"
