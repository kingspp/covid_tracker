from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from dashboard.app.server.constants import ModelConstants
from dashboard.app.server import *
import datetime
from covid19.utils import calc_n_days_after_date
import numpy as np

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
        print('pred ', pred)
        return pred

    def algorithm(week_predictions, ethnic_age_groups_df):
        # ethnic_age_groups_df['age_aggregated'] = ethnic_age_groups_df
        return np.mean(list(week_predictions.values()))

    def fetch_ethnic_age_data(fips):
        ethnic_age_grps = county_ethnicity_n_age_grps_data[county_ethnicity_n_age_grps_data['COUNTY'] == fips]
        ethnic_age_grps.drop(['STATE', 'COUNTY', 'STNAME', 'CTYNAME'], axis=1, inplace=True)
        return ethnic_age_grps

    week_predictions = {}
    state_county = userdetails.state_name + "_" + userdetails.county_name
    county = county_data[county_data.index == state_county]
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

    ethnic_age_groups_df = fetch_ethnic_age_data(fips)
    mean_pred = algorithm(week_predictions, ethnic_age_groups_df)
    return {'p_score': mean_pred}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

user = UserDetails
user.county_name = 'Worcester'
user.state_name = 'Massachusetts'
print(forecast(user))
