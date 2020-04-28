from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from dashboard.app.server.constants import ModelConstants
from dashboard.app.server import *
import datetime
from covid19.utils import calc_n_days_after_date, get_time_series_cols
import itertools

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/{counties}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


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
        print(f'No data for {state_county}')
        return 0
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


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# age_dict = {1: "0-4", 2: "5-9", 3: "10-14", 4: "15-19", 5: "20-24", 6: "25-29", 7: "30-34", 8: "35-39", 9: "40-44",
#             10: "45-49", 11: "50-54", 12: "55-59", 13: "60-64", 14: "65-69", 15: "70-74", 16: "75-79", 17: "80-84",
#             18: "85"}
# ethnic_groups = {
#     "WA_MALE": "White Male",
#     "WA_FEMALE": "White Female",
#     "BA_MALE": "Black or African Male",
#     "BA_FEMALE": "Black or African Female",
#     "IA_MALE": "American Indian and Alaska Native Male",
#     "IA_FEMALE": "American Indian and Alaska Native Female ",
#     "AA_MALE": "Asian Male",
#     "AA_FEMALE": "Asian Female",
#     "NA_MALE": "Native Hawaiian and Other Pacific Islander Male",
#     "NA_FEMALE": "Native Hawaiian and Other Pacific Islander Female",
#     "H_MALE": "Hispanic Male",
#     "H_FEMALE": "Hispanic Female"
# }
# d = pd.read_csv(
#         '/Users/badgod/badgod_documents/github/covid19_research/covid19/data/processed_confirmed_cases_data_apr26th.csv')
# states = list(d['state_county'].values)
# all_list = [states, list(age_dict.values()), list(ethnic_groups.keys())]
# all_list = list(itertools.product(*all_list))
# with open('data.txt', 'w') as op_file:
#     for grp in all_list:
#         user = UserDetails
#         user.county_name = grp[0].split('_')[1]
#         user.state_name = grp[0].split('_')[1]
#         user.age_group = grp[1]
#         user.ethnicity = grp[2]
#         score = forecast(user)
#         print(f'{user.state_name} - {user.county_name} - {user.age_group} - {user.ethnicity} --> {score}', file=op_file)
#
