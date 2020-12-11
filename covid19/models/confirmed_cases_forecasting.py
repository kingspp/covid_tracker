# -*- coding: utf-8 -*-
"""
@created on: 4/26/20,
@author: Shreesha N,
@version: v0.0.1
@system name: badgod
Description:

..todo::

"""

# All imports
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
from covid19.utils import calc_n_days_after_date

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
TOTAL_HISTORY = 90  # in days
COUNTY_DEMOGRAPHICS_COLUMNS = ["county_rank", "jhu_county_population", "poverty_percent_state", "unemployment_rate",
                               "total_unemployed", "median_household_income_perc_of_state", "median_household_income",
                               "emergency_declation_type", "emergency_declaration_date", "staffed_beds",
                               "licenced_beds",
                               "icu_beds", "average_ventilator_used_per_hospital", "poverty_rate"]


def prepare_demogs_data():
    # county_demogs = json.load(open('/Users/badgod/badgod_documents/Datasets/covid19/county_demog.json'))
    # result = pd.DataFrame(county_demogs)
    # result.to_csv("/Users/badgod/badgod_documents/Datasets/covid19/county_demog.csv", index=False)
    county_demog = pd.read_csv("../data/county_demog.csv")
    county_demog_US = county_demog[county_demog['country'] == 'US']
    county_demog_US = county_demog_US.replace('', np.nan)

    # Drop columns not useful for modelling
    drop_cols = ['county_population', 'county_r0', 'uid', 'iso2', 'iso3', 'code3', 'url', 'country', 'latitude',
                 'longitude', 'infographics_population', 'infographics_date', 'emergency_declaration_notes']
    # emergency_declaration_notes -> this column can be made use of to derive features using NLP
    county_demog_US = county_demog_US.drop(drop_cols, axis=1)

    # Dropping rows which have limited data. Come back here and handle it differently instead of removing
    county_demog_clean = county_demog_US.dropna()
    county_demog_clean['fips'] = county_demog_clean['fips'].astype(int)
    return county_demog_clean


def prepare_confirmed_cases_data():
    CONFIRMED_US = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    confirmed_us = pd.read_csv(CONFIRMED_US)
    print(f'Data available till is {confirmed_us.columns[-1]}')
    drop_cols_confirmed = ['UID', 'iso2', 'iso3', 'code3', 'Admin2', 'Country_Region', 'Lat', 'Long_', 'Combined_Key',
                           'Province_State']
    confirmed_us = confirmed_us.dropna()
    confirmed_us_clean = confirmed_us.drop(drop_cols_confirmed, axis=1)
    confirmed_us_clean.rename({'FIPS': 'fips'}, axis=1, inplace=True)
    confirmed_us_clean['fips'] = confirmed_us_clean['fips'].astype(int)
    return confirmed_us_clean


def prepare_final_data(county_demog_clean, confirmed_us_clean):
    confirmed_cases_usa = pd.merge(county_demog_clean, confirmed_us_clean, on='fips')
    confirmed_cases_usa = encode_based_on_risk(confirmed_cases_usa)
    confirmed_cases_usa = encode_emergency_date(confirmed_cases_usa)
    emergency_declation_type_encoding = {'Govt Ordered Community Quarantine': 0, 'Govt Directed Social Distancing': 1}
    confirmed_cases_usa['emergency_declation_type'] = confirmed_cases_usa['emergency_declation_type'].apply(
            lambda x: emergency_declation_type_encoding[x])

    delta_cols = [x for x in confirmed_cases_usa.columns if '/' in x][1:]
    confirmed_cases_usa_delta = confirmed_cases_usa.copy()
    confirmed_cases_usa_delta[delta_cols] = confirmed_cases_usa[delta_cols].diff(axis=1)
    confirmed_cases_usa_delta.fillna(0, inplace=True)
    return confirmed_cases_usa_delta


def dynamic(features, end_date, label_col='', test=False):
    time_series_cols = [x for x in features.columns if x not in COUNTY_DEMOGRAPHICS_COLUMNS]
    static_data = features[COUNTY_DEMOGRAPHICS_COLUMNS]

    time_series_data = get_history_data(features[time_series_cols], end_date)
    total_data = static_data.join(time_series_data)
    print(f'Start date: {time_series_data.columns[0]} -- End date: {end_date} -- Label: {label_col}')
    if test:
        return total_data
    else:
        return total_data, features[label_col]


def get_history_data(df, end_date):
    # TODO: fix the unknown bug here - end_date is being ignored
    cols = list(df.columns)
    end_date_idx = cols.index(end_date) + 1
    start_date_idx = end_date_idx - TOTAL_HISTORY
    if start_date_idx < 0:
        raise Exception(f"Invalid end date -> {end_date}. Start date index resulted in {start_date_idx}")
    required_cols = cols[start_date_idx:end_date_idx]
    return df[required_cols]


def encode_emergency_date(df):
    """
    rank emergency_declaration_date. Sorted based on when emergency was announced. Earlier the better.
    confirmed_cases_usa['emergency_declaration_date'] = pd.to_datetime(confirmed_cases_usa['emergency_declaration_date'])
    """
    emergency_date_ranking = {}
    dates = list(set(df['emergency_declaration_date'].unique()))
    prev_val, rank = dates[0], 0
    for k in dates:
        if k == prev_val:
            emergency_date_ranking[k] = rank
        else:
            rank += 1
            prev_val = k
            emergency_date_ranking[k] = rank
    df['emergency_declaration_date'] = df['emergency_declaration_date'].apply(lambda x: emergency_date_ranking[x])
    return df


def encode_based_on_risk(df):
    df['total_confirmed'] = 0
    date_columns = [col for col in df.columns if '/' in col]
    # get the cummulative sum of cases from start date till now
    df['total_confirmed'] = df[date_columns].apply(np.sum, axis=1)

    # create dictionary in with key as state+county and value as total confirmed cases
    county_risk = {f'{x[0]}_{x[1]}': x[2] for x in df[['state', 'county', 'total_confirmed']].itertuples(index=False)}

    # sort based on value in reverse order
    d = {k: v for k, v in sorted(county_risk.items(), key=lambda item: item[1])}

    # rank state+counties on their confirmed cases count. Higher the rank riskier it is. Confirmed delta change from previous
    # county's cases and add 10% of the delta to rank variable
    prev_val, rank = list(d.values())[0], 0
    for k, v in d.items():
        if v == prev_val:
            d[k] = [v, rank]
        else:
            rank += int((v - prev_val) * 0.1)
            prev_val = v
            d[k] = [v, rank]

    # df[['state','county']].apply(lambda x:x['state'])
    county_rank = df[['state', 'county']].apply(lambda x: d[x['state'] + "_" + x['county']][1], axis=1)
    df.insert(0, 'county_rank', county_rank)

    # drop state, county, total_confirmed columns
    df.drop(['total_confirmed'], axis=1, inplace=True)
    return df


def save_processed_file(df):
    df['state_county'] = df[['state', 'county']].apply(lambda x: x['state'] + '_' + x['county'], axis=1)
    df.drop(['state', 'county'], axis=1, inplace=True)

    county_ranking_json = {}

    def add_to_json(x):
        county_ranking_json[x['state_county']] = x['county_rank']

    # Save county ranks in json for further lookup
    df[['state_county', 'county_rank']].apply(lambda x: add_to_json(x), axis=1)
    json.dump(county_ranking_json, open('../data/county_ranking_map.json', 'w'), indent=4)

    col = df.pop('state_county')
    df.insert(0, col.name, col)
    df.to_csv('../data/processed_confirmed_cases_data_oct19.csv', index=False)
    df.drop('fips', axis=1, inplace=True)
    return df


def print_test_stats(inp_data_columns, label_column, test_error=None):
    time_series_col = [x for x in inp_data_columns if '/' in x]
    print(
            f'Data from {time_series_col[0]} to {time_series_col[-1]} was used. Predicted for {label_column}. Error: {test_error}')


class RFModel:
    def __init__(self):
        self.rf = RandomForestRegressor(n_estimators=1000, random_state=42)

    def _fit(self, x, y):
        self.rf.fit(x, y)

    def _evaluate(self, x, y):
        preds = self.rf.predict(x)
        errors = np.mean(abs(preds - y))
        return errors, preds

    def _predict(self, x):
        pass

    def _print_stats(self, x, y):
        r_square = self.rf.score(x, y)
        err, _ = self._evaluate(x, y)
        print(f'Error: {np.mean(err)}\nR-square: {r_square}')

    def _save(self):
        print('Saving model file ...')
        pickle.dump(self.rf, open(model_save_name, 'wb'))


def run():
    county_demog_clean = prepare_demogs_data()
    confirmed_us_clean = prepare_confirmed_cases_data()
    confirmed_cases_usa_delta = prepare_final_data(county_demog_clean, confirmed_us_clean)
    confirmed_cases_usa_delta = save_processed_file(confirmed_cases_usa_delta)

    train_features, test_features = train_test_split(confirmed_cases_usa_delta, test_size=0.2)
    # train_features, test_features = train_features.head(rows_to_consider), test_features.head(
    #         rows_to_consider)

    label_col = train_features.columns[-1]  # '4/26/20'
    end_date = train_features.columns[-2]  # '4/25/20'
    train_data, train_label = dynamic(train_features, end_date, label_col)
    test_data, test_label = dynamic(test_features, end_date, label_col)
    print(train_data.shape, train_label.shape)
    print(test_data.shape, test_label.shape)

    print(list(train_data.columns))
    json.dump({'columns': list(train_data.columns)}, open('../data/columns_used.json', 'w'))

    model = RFModel()
    model._fit(train_data.values, train_label.values)
    model._print_stats(train_data.values, train_label.values)
    model._save()

    test_err, test_preds = model._evaluate(test_data.values, test_label.values)
    print_test_stats(test_data.columns, label_col, test_err)

    today_date = '4/26/20'
    # Shifting by one day
    for _ in range(0, 4):
        # Replacing predictions with existing data
        test_features[label_col] = pd.Series(test_preds, index=test_label.index, dtype=int)

        label_col = calc_n_days_after_date(today_date, n_days=1)

        test_data = dynamic(test_features, end_date=today_date, label_col=label_col, test=True)
        test_preds = model._predict(test_data.values)
        print_test_stats(test_data.columns, label_col)

        today_date = label_col  # Using the predicted data to predict next day cases
        print('----' * 20)


    # Get the assumptions from Kevin

    age_admission_rate = {
        "< 18": {
            "ventilator":5,
            "icu":10,
            "hospitalization": 60,
            "normal":25
        },
        "18-44": {
            "ventilator": 5,
            "icu": 10,
            "hospitalization": 60,
            "normal": 25
        },
        "44-70": {
            "ventilator": 5,
            "icu": 10,
            "hospitalization": 60,
            "normal": 25
        },
        "70+": {
            "ventilator": 5,
            "icu": 10,
            "hospitalization": 60,
            "normal": 25
        }
    }

    res = {}
    for age_admission_r, vals in age_admission_rate.items():
        for stage in vals:
            res[age_admission_r] = stage*test_preds









if __name__ == '__main__':
    model_save_name = 'rf_model.pk'
    rows_to_consider = 10
    run()
