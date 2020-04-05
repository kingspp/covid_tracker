import requests
from covid19 import COVID19_MODULE_PATH

def fetch_data_and_save(url, file_path):
    response = requests.get(url)
    with open(COVID19_MODULE_PATH + f'/data/{file_path}', 'wb') as f:
        f.write(response.content)



url_protein = "https://www.ncbi.nlm.nih.gov/genomes/VirusVariation/vvsearch2/?q=*:*&fq=%7B!tag=SeqType_s%7DSeqType_s:(%22Protein%22)&fq=VirusLineageId_ss:(2697049)&cmd=download&sort=SourceDB_s%20desc,CreateDate_dt%20desc&dlfmt=csv&fl=Accession:id,Release_Date:CreateDate_dt,Species:VirusSpecies_s,Genus:VirusGenus_s,Family:VirusFamily_s,Length:SLen_i,Sequence_Type:SourceDB_s,Nuc_Completeness:Completeness_s,Genotype:Serotype_s,Segment:Segment_s,Authors:Authors_csv,Publications:PubMed_csv,Geo_Location:CountryFull_s,Host:Host_s,Isolation_Source:Isolation_csv,Collection_Date:CollectionDate_s,BioSample:BioSample_s,GenBank_Title:Definition_s"
url_nucleotide = "https://www.ncbi.nlm.nih.gov/genomes/VirusVariation/vvsearch2/?q=*:*&fq=%7B!tag=SeqType_s%7DSeqType_s:(%22Nucleotide%22)&fq=VirusLineageId_ss:(2697049)&cmd=download&sort=SourceDB_s%20desc,CreateDate_dt%20desc&dlfmt=csv&fl=Accession:id,Release_Date:CreateDate_dt,Species:VirusSpecies_s,Genus:VirusGenus_s,Family:VirusFamily_s,Length:SLen_i,Sequence_Type:SourceDB_s,Nuc_Completeness:Completeness_s,Genotype:Serotype_s,Segment:Segment_s,Authors:Authors_csv,Publications:PubMed_csv,Geo_Location:CountryFull_s,Host:Host_s,Isolation_Source:Isolation_csv,Collection_Date:CollectionDate_s,BioSample:BioSample_s,GenBank_Title:Definition_s"

fetch_data_and_save(url=url_protein, file_path='protein_latest.csv')
fetch_data_and_save(url=url_nucleotide, file_path='nucleotide_latest.csv')




