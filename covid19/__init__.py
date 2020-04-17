import os
import json
COVID19_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

from covid19.data import NucleotideData
from covid19.data import ProteinData

COUNTRIES = json.load(open(os.path.join(COVID19_MODULE_PATH,"data", "COUNTRIES.json")))


nucleotide_data = NucleotideData()
protein_data = ProteinData()