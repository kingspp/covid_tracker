import pandas as pd
import os
from covid19 import COVID19_MODULE_PATH

class NucleotideData(object):

    def __new__(cls, *args, **kwargs):
        df = pd.read_csv(os.path.join(COVID19_MODULE_PATH, 'data', 'nucleotide_latest.csv'))
        # df.sample(frac=1)
        return df

class ProteinData():
    def __new__(cls, *args, **kwargs):
        df = pd.read_csv(os.path.join(COVID19_MODULE_PATH, 'data', 'protein_latest.csv'))
        # df.sample(frac=1)
        return df