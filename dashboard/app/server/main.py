from fastapi import FastAPI
from covid19 import database as db
from fastapi.middleware.cors import CORSMiddleware
from scipy.special import expit
import json
import operator
from covid19 import COUNTIES, ETHNICITIES, COVID19_DATA_PATH
import random
from fastapi import FastAPI

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


@app.get("/v1/ethnicity")
def get_ethnicity():
    # counties=[]
    # coll = db.get_collection("county_demographics")
    # for coll in coll.find({"country":"US"}):
    #     counties.append(coll["combined_key"].replace("|", ", "))
    # with open('/Users/prathyushsp/Git/covid19_research/covid19/data/COUNTIES.json', 'w') as f:
    #     json.dump(counties, f, indent=2)
    return {'data': ETHNICITIES}


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
def get_currencies():
    return {'data': json.load(open(COVID19_DATA_PATH + '/' + 'crypto.json'))}


@app.get("/v1/mobility")
def get_mobility():
    return {'data': json.load(open(COVID19_DATA_PATH + '/ui/' + 'mobility.json'))}


class UserDetails(BaseModel):
    state_name: str = None
    county_name: str = None
    ethnicity: str = None
    age_group: str = None  # Eg: "0-5", "10-15"


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

        return groups_percentage * new_cases

    def fetch_ethnic_age_data(fips):
        ethnic_age_grps = county_ethnicity_n_age_grps_data[county_ethnicity_n_age_grps_data['fips'] == fips]
        if len(ethnic_age_grps) == 0:
            print(f'No data for {fips}')
            raise ValueError(
                    'Sorry! We have very limited data for your county. At this moment, we will not be able to forecast. Try again later')
        ethnic_age_grps.drop(['STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'fips'], axis=1, inplace=True)
        return ethnic_age_grps

    week_predictions = {}
    state_county = userdetails.state_name + "_" + userdetails.county_name
    age_grp = userdetails.age_group
    ethnicity = userdetails.ethnicity
    county = county_data[county_data.index == state_county]
    if len(county) == 0:
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
        week_predictions[label_col] = test_preds[0]
        county[label_col] = pd.Series(test_preds, dtype=int, index=county.index)
        county = dynamic(county)
        date = label_col

    mean_pred = algorithm(week_predictions, fips, age_grp, ethnicity)
    return {'p_score': mean_pred}


@app.get('/v1/variable_importance')
def get_variable_importance():
    columns = json.load(open(f'{COVID19_DATA_PATH}/columns_used.json'))['columns']
    importances = rf_model.feature_importances_
    imp_dict = {x: y for x, y in zip(columns, importances) if '/' not in x}
    imp_dict_sorted = sorted(imp_dict.items(), key=operator.itemgetter(1), reverse=True)
    return {x: y for x, y in imp_dict_sorted}
