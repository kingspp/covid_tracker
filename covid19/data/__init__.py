import pandas as pd
import os
from covid19 import COVID19_MODULE_PATH
from dataclasses import dataclass


class NucleotideData(object):
    def __new__(cls, *args, **kwargs):
        df = pd.read_csv(os.path.join(COVID19_MODULE_PATH, 'data', 'nucleotide_latest.csv'))
        return df


class ProteinData():
    def __new__(cls, *args, **kwargs):
        df = pd.read_csv(os.path.join(COVID19_MODULE_PATH, 'data', 'protein_latest.csv'))
        return df


@dataclass
class Religion():
    christians: float = ""
    muslims: float = ""
    unaffiliated: float = ""
    hindus: float = ""
    buddhists: float = ""
    folk_religions: float = ""
    other_religions: float = ""
    jews: float = ""

@dataclass
class WorldDemographics():
    world_population: float = ""
    world_male_population: float = ""
    world_female_population: float = ""
    world_population_density: float = ""
    world_area: str = ""
    world_r0: float = ""
    number_of_continents: int = ""
    number_of_countries: int = ""
    religion:dict=""
    world_median_age: float = ""


@dataclass
class ContinentDemographics():
    continent: str = ""
    continent_population: float = ""
    continent_male_population: float = ""
    continent_female_population: float = ""
    continent_population_density: float = ""
    continent_area: str = ""
    continent_r0: float = ""
    number_of_countries: int = ""
    religion:dict=""
    continent_median_age:float=""




@dataclass
class CountryDemographics():
    country: str
    continent: str = ""
    country_area: float = ""
    country_government_type: str = ""
    country_r0: float = ""
    country_median_age: float = ""
    country_prime_leader_gender: str = ""
    country_male_population: float = ""
    country_female_population: float = ""
    country_population: float = ""
    country_population_density: float = ""
    latitude: float = ""
    longitude: float = ""
    religion:dict=""
    uid:str=""
    iso2:str=""
    iso3:str=""
    code3:str=""
    fips:str=""
    county:str=""
    state:str=""
    jhu_country_population:str=""
    lockdown_start_date:str=""
    lockdown_end_date:str=""

@dataclass
class CountyDemographics():
    country: str=""
    state:str=""
    county: str=""
    county_population: float=""
    latitude: float=""
    longitude: float=""
    county_r0: float=""
    uid: str = ""
    iso2: str = ""
    iso3: str = ""
    code3: str = ""
    fips: str = ""
    jhu_county_population: str = ""
    poverty_percent_state: float = ""
    infographics_date: str = ""
    unemployment_rate: float = ""
    total_unemployed: float = ""
    median_household_income_perc_of_state: float = ""
    median_household_income: float = ""
    emergency_declation_type:str=""
    emergency_declaration_date:str=""
    emergency_declaration_notes:str=""
    url:str=""
    # state_tested: str = ""
    # state_recovered: str = ""
    # state_confirmed: str = ""
    # state_deaths: str = ""
    infographics_population:float=""
    staffed_beds: float = ""
    licenced_beds: float = ""
    icu_beds: float = ""
    average_ventilator_used_per_hospital: float = ""
    poverty_rate:float=""

@dataclass
class NCBINucleotide():
    accession:str=""
    release_date:str=""
    species:str=""
    genus:str=""
    family:str=""
    length:str=""
    sequence_type:str=""
    nuc_completeness:str=""
    genotype:str=""
    segment:str=""
    authors:str=""
    publications:str=""
    country:str=""
    host:str=""
    isolation_source:str=""
    collection_date:str=""
    bio_sample:str=""
    gen_bank_title:str=""
    county:str=""
    type: str = "nucleotide"



@dataclass
class NCBIProtein():
    accession:str=""
    release_date:str=""
    species:str=""
    genus:str=""
    family:str=""
    length:str=""
    sequence_type:str=""
    nuc_completeness:str=""
    genotype:str=""
    segment:str=""
    authors:str=""
    publications:str=""
    country:str=""
    host:str=""
    isolation_source:str=""
    collection_date:str=""
    bio_sample:str=""
    gen_bank_title:str=""
    county:str=""
    type:str="protein"

@dataclass
class GoogleMobilityRecords():
    country_code:str=""
    country:str=""
    sub_region_1:str=""
    sub_region_2:str=""
    date:str=""
    retail_and_recreation_percent_change_from_baseline:int=""
    grocery_and_pharmacy_percent_change_from_baseline:int=""
    parks_percent_change_from_baseline:int=""
    transit_stations_percent_change_from_baseline:int=""
    workplaces_percent_change_from_baseline:int=""
    residential_percent_change_from_baseline:int=""


@dataclass
class Statistics():
    country:str=""
    province:str=""
    date:str=""
    confirmed:float=""
    recovered:float=""
    death:float=""
    active:float=""
    confirmed_delta:float=""
    recovered_delta: float = ""
    death_delta: float = ""
    active_delta: float = ""
    county: float = ""
    recovery_rate:float=""
    death_rate: float = ""
    active_rate:float=""
    confirmed_by_population: float = ""
    deaths_by_population: float = ""
    active_by_population: float = ""
    recovered_by_population: float = ""