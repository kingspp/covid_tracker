# COVID19 Reseach

#### Requirements:
1. Python 3.7+

## Documents
[Proposal](https://docs.google.com/document/d/10DEj1amBY032zPM7av0jZpFpkQ9IhZFcYuKpy6hm4qo/edit?usp=sharing)
[BibTex]()

## Dashboard

Monitoring Tool for Corona Virus
* Built using HTML5/CSS3/JS Stack
* Hosted in Codepen


## Data 

1. NCBI Mutation Data

```bash
# How to update the data
python3 covid19/data/fetch_ncbi_data.py
```

```python
# How to use the dataset
from covid19.data import NucleotideData
from covid19.data import ProteinData

nucleotide_data = NucleotideData()
protein_data = ProteinData()
```