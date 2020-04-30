from fastapi import FastAPI
from covid19 import database as db
from fastapi.middleware.cors import CORSMiddleware
from scipy.special import expit
import json
import operator
from covid19 import COUNTIES, ETHNICITIES, COVID19_DATA_PATH
import random
from fastapi import FastAPI
import numpy as np

import uvicorn
from pydantic import BaseModel
from dashboard.app.server.constants import ModelConstants
from dashboard.app.server import *
import datetime
from covid19.utils import calc_n_days_after_date, get_time_series_cols
import itertools

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0:8877",
    "http://104.251.210.60:8877"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/county")
def get_county():
    # counties=[]
    # coll = db.get_collection("county_demographics")
    # for coll in coll.find({"country":"US"}):
    #     counties.append(coll["combined_key"].replace("|", ", "))
    # with open('/Users/prathyushsp/Git/covid19_research/covid19/data/COUNTIES.json', 'w') as f:
    #     json.dump(counties, f, indent=2)
    return {'data': COUNTIES}


@app.get("/v1/age")
def get_age_group():
    return {'data': [{'key': '1', 'val': '0-4'},
                     {'key': '2', 'val': '5-9'},
                     {'key': '3', 'val': '10-14'},
                     {'key': '4', 'val': '15-19'},
                     {'key': '5', 'val': '20-24'},
                     {'key': '6', 'val': '25-29'},
                     {'key': '7', 'val': '30-34'},
                     {'key': '8', 'val': '35-39'},
                     {'key': '9', 'val': '40-44'},
                     {'key': '10', 'val': '45-49'},
                     {'key': '11', 'val': '50-54'},
                     {'key': '12', 'val': '55-59'},
                     {'key': '13', 'val': '60-64'},
                     {'key': '14', 'val': '65-69'},
                     {'key': '15', 'val': '70-74'},
                     {'key': '16', 'val': '75-79'},
                     {'key': '17', 'val': '80-84'},
                     {'key': '18', 'val': '85'}]}


@app.get("/v1/ethnicity")
def get_ethnicity():
    # counties=[]
    # coll = db.get_collection("county_demographics")
    # for coll in coll.find({"country":"US"}):
    #     counties.append(coll["combined_key"].replace("|", ", "))
    # with open('/Users/prathyushsp/Git/covid19_research/covid19/data/COUNTIES.json', 'w') as f:
    #     json.dump(counties, f, indent=2)
    return {'data': [{'key': 'WA_MALE', 'val': 'White Male'},
                     {'key': 'WA_FEMALE', 'val': 'White Female'},
                     {'key': 'BA_MALE', 'val': 'Black or African Male'},
                     {'key': 'BA_FEMALE', 'val': 'Black or African Female'},
                     {'key': 'IA_MALE', 'val': 'American Indian and Alaska Native Male'},
                     {'key': 'IA_FEMALE', 'val': 'American Indian and Alaska Native Female '},
                     {'key': 'AA_MALE', 'val': 'Asian Male'},
                     {'key': 'AA_FEMALE', 'val': 'Asian Female'},
                     {'key': 'NA_MALE', 'val': 'Native Hawaiian and Other Pacific Islander Male'},
                     {'key': 'NA_FEMALE',
                      'val': 'Native Hawaiian and Other Pacific Islander Female'},
                     {'key': 'H_MALE', 'val': 'Hispanic Male'},
                     {'key': 'H_FEMALE', 'val': 'Hispanic Female'}]}


@app.get("/v1/modelVariables")
def get_variables():
    return {'data': [[e[:5], random.uniform(0, 1)] for e in ETHNICITIES]}


@app.get("/v1/stocks")
def get_stocks():
    return {'data': json.load(open(COVID19_DATA_PATH + '/' + 'stocks.json'))}


@app.get("/v1/global_confirmed")
def get_global_confirmed():
    return {'data': json.load(open(COVID19_DATA_PATH + '/' + 'world_count.json'))}


@app.get("/v1/currencies")
def get_currencies():
    return {'data': json.load(open(COVID19_DATA_PATH + '/' + 'currencies.json'))}


@app.get("/v1/crypto")
def get_crypto():
    return {'data': json.load(open(COVID19_DATA_PATH + '/' + 'crypto.json'))}


@app.get("/v1/mobility")
def get_mobility():
    return {'data': json.load(open(COVID19_DATA_PATH + '/ui/' + 'mobility.json'))}


class UserDetails(BaseModel):
    state_name: str = None
    county_name: str = None
    ethnicity: str = None
    age_group: str = None  # Eg: "0-5", "10-15"


def algorithm2(new_cases, fips, age_grp, ethnicity):
    percentage_affected_in_group = \
        ethnic_age_splits_affected[ethnic_age_splits_affected["Ethnicity"] == ethnicity][age_grp].values[
            0] / \
        np.sum(ethnic_age_splits_affected[age_dict].values)

    possible_new_cases_in_group = new_cases * percentage_affected_in_group

    county_level = county_ethnicity_n_age_grps_data_new[
        county_ethnicity_n_age_grps_data_new['fips'] == fips]
    total_population_in_group = county_level[county_level['cdc_age_groups'] == age_grp][ethnicity].values[0]
    county_population = np.sum(county_level[ethnic_groups].values)

    percentage_ethnic_age_grp_in_county = total_population_in_group / county_population

    # County total infected count in the county
    county_demog = county_data[county_data['fips'] == fips]
    time_series_cols = get_time_series_cols(county_demog)
    total_infected = county_demog[time_series_cols].sum(axis=1).values[0]

    total_unaffected = county_population - total_infected
    total_unaffected_in_grp = total_unaffected * percentage_ethnic_age_grp_in_county

    if total_unaffected_in_grp == 0 or possible_new_cases_in_group == 0:
        return -100
    else:
        return possible_new_cases_in_group / total_unaffected_in_grp


@app.post("/v1/forecast")
def forecast(userdetails: UserDetails):
    def dynamic(df):
        time_series_cols = [col for col in df.columns if '/' in col]
        time_series_cols = time_series_cols[-ModelConstants.TIME_SERIES_LEN:]
        static_cols = [col for col in df.columns if '/' not in col]
        df = df[static_cols + time_series_cols]
        return df

    def predict(data):
        pred = rf_model.predict(data)
        return pred

    def algorithm(week_predictions, fips, age_grp, ethnicity):

        def get_total_population(df):
            population_cols = [col for col in df.columns if 'MALE' in col or 'FEMALE' in col]
            total_population = df[population_cols].sum()
            return total_population.values[0]

        def calc_group_percentage_against_total_population(df, age_grp, ethnicity, total_uninfected):
            grp_population = df[df['AGEGRP'] == age_grp][ethnicity].values[0]
            return grp_population / total_uninfected

        new_cases = sum(list(week_predictions.values()))

        # County total infected count in the county
        county_demog = county_data[county_data['fips'] == fips]
        time_series_cols = get_time_series_cols(county_demog)
        total_infected = county_demog[time_series_cols].sum(axis=1).values[0]

        # Now get total population from ethnic groups
        # Depending on this population data is not a good idea as there are cases where
        # same person is counted in multiple ethnic groups
        ethnic_age_groups_df = fetch_ethnic_age_data(fips)
        total_population = get_total_population(ethnic_age_groups_df)
        total_uninfected = total_population - total_infected
        groups_percentage = calc_group_percentage_against_total_population(ethnic_age_groups_df, age_grp, ethnicity,
                                                                           total_uninfected)
        # print(groups_percentage, new_cases)
        return groups_percentage * new_cases

    def fetch_ethnic_age_data(fips):
        ethnic_age_grps = county_ethnicity_n_age_grps_data[county_ethnicity_n_age_grps_data['fips'] == fips]
        if len(ethnic_age_grps) == 0:
            print(f'No data for {fips}')
            raise ValueError(
                'Sorry! We have very limited data for your county. At this moment, we will not be able to forecast. Try again later')
        ethnic_age_grps.drop(['STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'fips'], axis=1, inplace=True)
        return ethnic_age_grps

    def get_population_age_wise(df):
        population_cols = [col for col in df.columns if 'MALE' in col or 'FEMALE' in col]
        df['total'] = df[population_cols].sum(axis=1)
        age_splits = {age: total_population for age, total_population in df[['AGEGRP', 'total']].values}
        df.drop('total', axis=1, inplace=True)
        return age_splits

    def get_population_ethnicity_wise(df):
        df.drop('AGEGRP', axis=1, inplace=True)
        return df.sum(axis=0).to_dict()

    def mask_keys(ethnic_dict):
        keys = {'WA_MALE': 'White Male',
                'WA_FEMALE': 'White Female',
                'BA_MALE': 'Black or African Male',
                'BA_FEMALE': 'Black or African Female',
                'IA_MALE': 'American Indian and Alaska Native Male',
                'IA_FEMALE': 'American Indian and Alaska Native Female ',
                'AA_MALE': 'Asian Male',
                'AA_FEMALE': 'Asian Female',
                'NA_MALE': 'Native Hawaiian and Other Pacific Islander Male',
                'NA_FEMALE': 'Native Hawaiian and Other Pacific Islander Female',
                'H_MALE': 'Hispanic Male',
                'H_FEMALE': 'Hispanic Female'}
        return {keys[ethnic_group]: pop_count for ethnic_group, pop_count in ethnic_dict.items()}

    week_predictions = {}
    state_county = userdetails.state_name + "_" + userdetails.county_name
    age_grp = userdetails.age_group
    ethnicity = userdetails.ethnicity
    county = county_data[county_data.index == state_county]
    if len(county) == 0:
        # print('No data ', userdetails.county_name)
        # return 0
        raise ValueError(
                f'Sorry! We have very limited data for your {userdetails.county_name}. At this moment, we will not be able to forecast. Try again later')
    fips = int(county['fips'])  # Use fips to fetch data from ethnic and age groups file
    county.drop('fips', axis=1, inplace=True)
    county = dynamic(county)

    date = datetime.datetime.today()
    date = f'{date.month}/{date.day}/{str(date.year)[-2:]}'

    for i in range(7):
        label_col = calc_n_days_after_date(date, n_days=1)
        test_preds = predict(county.values)
        week_predictions[label_col] = int(test_preds[0])
        county[label_col] = pd.Series(test_preds, dtype=int, index=county.index)
        county = dynamic(county)
        date = label_col

    # mean_pred = algorithm(week_predictions, fips, age_grp, ethnicity)
    mean_pred = algorithm2(sum(week_predictions.values()), fips, age_grp, ethnicity)
    ethics_n_age_groups = fetch_ethnic_age_data(fips)
    age_wise_population = get_population_age_wise(ethics_n_age_groups)
    ethnicity_wise_population = get_population_ethnicity_wise(ethics_n_age_groups)
    final_json = {}
    final_json['week_forecasts'] = week_predictions
    final_json['p_score'] = mean_pred
    final_json['age_splits'] = age_wise_population
    final_json['ethnicity_splits'] = mask_keys(ethnicity_wise_population)
    return final_json


@app.get('/v1/variable_importance')
def get_variable_importance():
    columns = json.load(open(f'{COVID19_DATA_PATH}/columns_used.json'))['columns']
    importances = rf_model.feature_importances_
    imp_dict = {x: y for x, y in zip(columns, importances) if '/' not in x}
    imp_dict_sorted = sorted(imp_dict.items(), key=operator.itemgetter(1), reverse=True)
    return {x: y for x, y in imp_dict_sorted}


d = pd.read_csv(
        f'{COVID19_DATA_PATH}/processed_confirmed_cases_data_apr26th.csv')
states = list(d['state_county'].values)
state_count_fips_mapping = {s_c: f for s_c, f in d[['state_county', 'fips']].values}
age_dict = ["< 18", "18-44", "45-64", "65-74", "75+"]

ethnic_groups = [
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Native Hawaiian or other Pacific Islander",
    "White",
    "Other"]

u = UserDetails
u.ethnicity = 'Black or African American'
u.age_group = '45-64'
u.state_name = 'Indiana'
u.county_name = 'Cass'
result = forecast(u)
print(result)
# score = algorithm2(new_cases_total, state_count_fips_mapping[u.state_name + '_' + u.county_name], u.age_group,
#                    u.ethnicity)
# print(score)
# age_dict = ["< 18", "18-44", "45-64", "65-74", "75+"]
#
# ethnic_groups = [
#     "American Indian or Alaska Native",
#     "Asian",
#     "Black or African American",
#     "Native Hawaiian or other Pacific Islander",
#     "White",
#     "Other"]
# d = pd.read_csv(
#         f'{COVID19_DATA_PATH}/processed_confirmed_cases_data_apr26th.csv')
# states = list(d['state_county'].values)
# state_count_fips_mapping = {s_c: f for s_c, f in d[['state_county', 'fips']].values}
# all_list = [age_dict, ethnic_groups]
# all_list = list(itertools.product(*all_list))
#
# with open('predictions_county_wise_data.csv', 'w') as op_file:
#     for i, state_county in enumerate(states):
#         print(f'Processing {i}/{len(states)}')
#         user = UserDetails
#         user.county_name = state_county.split('_')[1]
#         user.state_name = state_county.split('_')[0]
#         week_total_cases = forecast(user)
#         for age_grp, ethnic_grp in all_list:
#             prob = algorithm2(week_total_cases, state_count_fips_mapping[state_county], age_grp=age_grp,
#                               ethnicity=ethnic_grp)
#             print(f'{user.state_name},{user.county_name},{age_grp},{ethnic_grp},{prob}',
#                   file=op_file)
