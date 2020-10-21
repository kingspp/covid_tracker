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
#         '/Users/badgod/badgod_documents/github/covid19_research/covid19/data/processed_confirmed_cases_data_oct19.csv')
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
