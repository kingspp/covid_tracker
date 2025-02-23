import pickle
from dashboard.app.server.constants import ModelConstants
import os
import json
import pandas as pd
from covid19.utils import file_exists_check

# Load the trained RF model when the webapp is instantiated
model_folder_basepath = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
rf_model_path = model_folder_basepath + '/' + ModelConstants.SAVE_PATH

file_exists_check(rf_model_path, 'Forecasting model file not found. Please specify a valid location.')
rf_model = pickle.load(open(rf_model_path, 'rb'))
print(f'Model loaded successfully. Path -> {rf_model_path}')

# Load county rank mapping json
county_rank_mapping_file = model_folder_basepath + '/' + ModelConstants.COUNTY_RANK_MAPPING_FILE
file_exists_check(county_rank_mapping_file, 'Counties riskiness mapping file not found.')
county_rank_mappings = json.load(open(county_rank_mapping_file))
print(f'County riskiness mappings loaded successfully. Path -> {county_rank_mapping_file}')

# Load processed county dataframe
county_processed_file = model_folder_basepath + '/' + ModelConstants.COUNTY_PROCESSED_DATA
file_exists_check(county_processed_file, 'Counties processed data file not found.')
county_data = pd.read_csv(county_processed_file)
county_data.set_index('state_county', inplace=True)
print(f'County processed data loaded successfully. Path -> {county_processed_file}')

# Load Ethnicity and Age groups data
county_ethnicity_n_age_grps_file = model_folder_basepath + '/' + ModelConstants.COUNTY_ETHNICITY_AND_AGE_GRPS
file_exists_check(county_ethnicity_n_age_grps_file, 'Counties Ethnicity and Age groups data file not found.')
county_ethnicity_n_age_grps_data = pd.read_csv(county_ethnicity_n_age_grps_file)
print(f'County Ethnicity and Age group data loaded successfully. Path -> {county_ethnicity_n_age_grps_file}')

# Load Ethnicity and Age groups data
county_ethnicity_n_age_grps_file_new = model_folder_basepath + '/' + ModelConstants.COUNTY_ETHNICITY_AND_AGE_GRPS_NEW
file_exists_check(county_ethnicity_n_age_grps_file_new, 'Counties Ethnicity and Age groups data file not found.')
county_ethnicity_n_age_grps_data_new = pd.read_csv(county_ethnicity_n_age_grps_file_new)
print(f'County Ethnicity and Age group data loaded successfully. Path -> {county_ethnicity_n_age_grps_file_new}')

# Load Ethnicity and Age groups data - affected
ethnic_age_splits_file = model_folder_basepath + '/' + ModelConstants.ETHNICITY_AGE_GRP_AFFECTED_DATA
file_exists_check(ethnic_age_splits_file,
                  'Ethnicity and Age groups affected with covid data file not found.')
ethnic_age_splits_affected = pd.read_csv(ethnic_age_splits_file)
print(f'Ethnicity and Age groups affected with covid data loaded successfully. Path -> {ethnic_age_splits_file}')


age_dict = ["< 18", "18-44", "45-64", "65-74", "75+"]

ethnic_groups = [
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Native Hawaiian or other Pacific Islander",
    "White",
    "Other"]