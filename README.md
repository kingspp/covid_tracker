# COVID19 Reseach

## Dashboard

Monitoring Tool for Corona Virus
* Built using HTML5/CSS3/JS Stack
* Hosted in Codepen


## Data 

1. NCBI Mutation Data

```bash
# How to update the data
covid19/data/fetch_ncbi_data.csv
```

```python
# How to use the dataset
from covid19.data import NucleotideData
from covid19.data import ProteinData

nucleotide_data = NucleotideData()
protein_data = ProteinData()
```