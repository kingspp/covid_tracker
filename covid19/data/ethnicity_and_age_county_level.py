# -*- coding: utf-8 -*-
"""
@created on: 4/27/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""

import pandas as pd

age_dict = {1: "0-4", 2: "5-9", 3: "10-14", 4: "15-19", 5: "20-24", 6: "25-29", 7: "30-34", 8: "35-39", 9: "40-44",
            10: "45-49", 11: "50-54", 12: "55-59", 13: "60-64", 14: "65-69", 15: "70-74", 16: "75-79", 17: "80-84",
            18: "85"}
ethnic_groups = {
    "WA_MALE": "White Male",
    "WA_FEMALE": "White Female",
    "BA_MALE": "Black or African Male",
    "BA_FEMALE": "Black or African Female",
    "IA_MALE": "American Indian and Alaska Native Male",
    "IA_FEMALE": "American Indian and Alaska Native Female ",
    "AA_MALE": "Asian Male",
    "AA_FEMALE": "Asian Female",
    "NA_MALE": "Native Hawaiian and Other Pacific Islander Male",
    "NA_FEMALE": "Native Hawaiian and Other Pacific Islander Female",
    "H_MALE": "Hispanic Male",
    "H_FEMALE": "Hispanic Female"
}
required_cols = ["STATE", "COUNTY", "STNAME", "CTYNAME", "AGEGRP"]

data = pd.read_csv('/Users/badgod/Downloads/cc-est2018-alldata.csv', encoding='latin-1')

latest = data[data['YEAR'] == 11]
latest = latest[latest['AGEGRP'] != 0]
latest['AGEGRP'] = latest['AGEGRP'].apply(lambda x: age_dict[x])
latest = latest[required_cols + list(ethnic_groups.keys())]
latest.to_csv('latest_ethnic_age_county_level_demog.csv', index=False)
