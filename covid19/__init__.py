import os

COVID19_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

from covid19.data import NucleotideData
from covid19.data import ProteinData


nucleotide_data = NucleotideData()
protein_data = ProteinData()