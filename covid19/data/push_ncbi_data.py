# Country Median Data
import json
from covid19.data import CountryDemographics, ContinentDemographics, WorldDemographics
from covid19 import COVID19_DATA_PATH, COUNTRIES
import pymongo
from covid19.utils import JsonEncoder
from covid19.data import NucleotideData, ProteinData, NCBINucleotide, NCBIProtein
import pandas as pd

NUCLEOTIDE_COUNTRY_MAPPER = json.load(open(COVID19_DATA_PATH+"/nucleotide_country_mapper.json"))

ndf = NucleotideData()
pdf = ProteinData()

nuc_collection = []
prot_collection = []

# NUC Collection
for row in ndf.iterrows():
    row = row[1].to_dict()
    if (row["Geo_Location"].__str__()!=float("nan").__str__()):
        row_c = row["Geo_Location"].split(":")
        country = row_c[0].strip()
        county = row_c[1].strip() if len(row_c)>1 else ""
        country = country if country in COUNTRIES else NUCLEOTIDE_COUNTRY_MAPPER[country]
        nuc_collection.append(NCBINucleotide(accession=row['Accession'],
                                             release_date=row['Release_Date'],
                                             species=row["Species"],
                                             genus=row['Genus'],
                                             family=row["Family"],
                                             length=row["Length"],
                                             sequence_type=row["Species"],
                                             nuc_completeness=row["Nuc_Completeness"],
                                             genotype=row["Genotype"],
                                             segment=row["Segment"],
                                             authors=row["Authors"],
                                             publications=row["Publications"],
                                             country=country,
                                             host=row["Host"],
                                             isolation_source=row["Isolation_Source"],
                                             collection_date=row["Collection_Date"],
                                             bio_sample=row["BioSample"],
                                             gen_bank_title=row["GenBank_Title"],
                                             county=county))


# Protein Collection
for row in pdf.iterrows():
    row = row[1].to_dict()
    if (row["Geo_Location"].__str__()!=float("nan").__str__()):
        row_c = row["Geo_Location"].split(":")
        country = row_c[0].strip()
        county = row_c[1].strip() if len(row_c)>1 else ""
        country = country if country in COUNTRIES else NUCLEOTIDE_COUNTRY_MAPPER[country]
        prot_collection.append(NCBIProtein(accession=row['Accession'],
                                             release_date=row['Release_Date'],
                                             species=row["Species"],
                                             genus=row['Genus'],
                                             family=row["Family"],
                                             length=row["Length"],
                                             sequence_type=row["Species"],
                                             nuc_completeness=row["Nuc_Completeness"],
                                             genotype=row["Genotype"],
                                             segment=row["Segment"],
                                             authors=row["Authors"],
                                             publications=row["Publications"],
                                             country=country,
                                             host=row["Host"],
                                             isolation_source=row["Isolation_Source"],
                                             collection_date=row["Collection_Date"],
                                             bio_sample=row["BioSample"],
                                             gen_bank_title=row["GenBank_Title"],
                                             county=county))

# print(json.dumps(nuc_collection[0], indent=2, cls=JsonEncoder))
# print(json.dumps(prot_collection[0], indent=2, cls=JsonEncoder))


def insert():
    client = pymongo.MongoClient(host="192.168.1.16")
    database = client.get_database("covid19_research")

    # Insert Nucleotide Collection
    database.drop_collection("ncbi_nucleotide")
    collection = database.get_collection("ncbi_nucleotide")
    for coll in nuc_collection:
        collection.insert(coll.__dict__)

    # Insert Protein Collection
    database.drop_collection("ncbi_protein")
    collection = database.get_collection("ncbi_protein")
    for coll in prot_collection:
        collection.insert(coll.__dict__)


insert()