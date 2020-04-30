# -*- coding: utf-8 -*-
"""
@created on: 4/28/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""

import pandas as pd

pd.set_option('display.max_columns', 100000)

data = pd.read_csv('latest_ethnic_age_county_level_demog.csv')

required_cols = ["STATE", "COUNTY", "CTYNAME", "STNAME", "fips", "cdc_age_groups"]

age_mapping = {
    "0-4": "< 18",
    "5-9": "< 18",
    "10-14": "< 18",
    "15-19": "< 18",
    "20-24": "18-44",
    "25-29": "18-44",
    "30-34": "18-44",
    "35-39": "18-44",
    "40-44": "18-44",
    "45-49": "45-64",
    "50-54": "45-64",
    "55-59": "45-64",
    "60-64": "45-64",
    "65-69": "65-74",
    "70-74": "65-74",
    "75-79": "75+",
    "80-84": "75+",
    "85": "75+"
}

data['cdc_age_groups'] = data['AGEGRP'].apply(lambda x: age_mapping[x])
# print(data.head())

data['state_county'] = data['STNAME'] + '_' + data['CTYNAME']

pop_cols = [x for x in data.columns if 'MALE' in x or 'FEMALE' in x]

ethnicity_to_group = {'White': ["WA_MALE", "WA_FEMALE"],
                      "American Indian or Alaska Native": ["IA_MALE", "IA_FEMALE"],
                      "Asian": ["AA_MALE", "AA_FEMALE"],
                      "Black or African American": ["BA_MALE", "BA_FEMALE"],
                      "Native Hawaiian or other Pacific Islander": ["NA_MALE", "NA_FEMALE"],
                      "Other": ["H_MALE", "H_FEMALE"]
                      }

final_df = []

# groups = data.groupby('cdc_age_groups')
# for id, g in groups:
#     print(g)
#     exit()
#     row = g[required_cols].iloc[1]
#     d = g[pop_cols].sum()
#     for eth in ethnicity_to_group.keys():
#         d[eth] = d[ethnicity_to_group[eth]].sum()
#     d = d.drop(pop_cols)
#     final_row = pd.concat([row, d], axis=0)
#     final_df.append(final_row)
#
# df = pd.concat(final_df, axis=1)
# print(df.head())
# data = data.head(n=100)

for id, g in data.groupby('state_county'):
    for idx, age_group in g.groupby('cdc_age_groups'):
        # print(age_group)

        row = age_group[age_group['cdc_age_groups'] == idx][required_cols].iloc[0]
        # print(row)
        # print('---')

        d = age_group[pop_cols].sum()
        for eth in ethnicity_to_group.keys():
            d[eth] = d[ethnicity_to_group[eth]].sum()
        d = d.drop(pop_cols)
        # print(d)
        final_row = pd.concat([row, d], axis=0)
        # print('FINAL ROW ***************************')
        # print(final_row)
        # print('FINAL ROW ***************************')
        # print(final_row)
        # exit()
        final_df.append(final_row)
        print('appending')

    # exit()

print(len(final_df))
df = pd.DataFrame(final_df, columns=["STATE", "COUNTY", "CTYNAME", "STNAME", "fips", "cdc_age_groups", "White",
                                     "American Indian or Alaska Native", "Asian", "Black or African American",
                                     "Native Hawaiian or other Pacific Islander", "Other"])
# print(df.head(n=10))

df.to_csv('county_ethnicity_age_groups_new.csv', index=False)