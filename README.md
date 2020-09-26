# COVID19 Reseach

![COVID 19 Research](https://raw.githubusercontent.com/kingspp/covid19_research/66dd5fbbbc9619337405a43070943bb33942e24c/dashboard/app/src/assets/demo.png)

#### Requirements:
1. Python 3.7+

## Documents
1. [Proposal](https://docs.google.com/document/d/10DEj1amBY032zPM7av0jZpFpkQ9IhZFcYuKpy6hm4qo/edit?usp=sharing)
2. [Data Sources and Attribute List](https://docs.google.com/spreadsheets/d/1vciQLHLW-a4RZnuwnnPHg9UxHwMUGm2xG9Ui_fUgXug/edit?usp=sharing)
3. [Presentation](https://github.com/kingspp/covid19_research/blob/master/DS%20502%20Final%20Project%20Group%207.pptx)
4. [Datasets](https://github.com/kingspp/covid19_research/tree/master/covid19/data)

## Dashboard

1. [COVID-19 Dashboard](http://104.251.210.60:8877/)


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
