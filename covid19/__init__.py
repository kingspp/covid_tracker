import os
import json
COVID19_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
COVID19_DATA_PATH = os.path.dirname(os.path.abspath(__file__))+"/data/"

from covid19.data import NucleotideData
from covid19.data import ProteinData
from pymongo import MongoClient

COUNTRIES = json.load(open(os.path.join(COVID19_MODULE_PATH,"data", "COUNTRIES.json")))
CONFIG = json.load(open(os.path.join(COVID19_MODULE_PATH, "config.json")))

client = MongoClient(host=CONFIG["mongo_db_config"]["configs"][CONFIG["mongo_db_config"]["use_config"]]["host"],
                     port=int(CONFIG["mongo_db_config"]["configs"][CONFIG["mongo_db_config"]["use_config"]]["port"]))
database = client.get_database(CONFIG["mongo_db_config"]["database"])

nucleotide_data = NucleotideData()
protein_data = ProteinData()