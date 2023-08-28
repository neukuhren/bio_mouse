import csv
import Bio
import pandas as pd
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from pathlib import Path

target_path = 'Mouse/'
list_of_cif = []
for file in Path(target_path).glob('*.cif'):
    dico = MMCIF2Dict(file)
    temp = pd.DataFrame.from_dict(dico, orient = 'index')
    temp = temp.transpose()
    temp.insert(0,'Filename', Path(file).stem)
    list_of_cif.append(temp)
df = pd.concat(list_of_cif)
df ['_ma_target_ref_db_details.gene_name'] = df ['_ma_target_ref_db_details.gene_name'].str[0]
df ['_ma_qa_metric_global.metric_value'] = df ['_ma_qa_metric_global.metric_value'].str[0]
new_df = df[['_ma_target_ref_db_details.gene_name', '_ma_qa_metric_global.metric_value']]
new_df.to_csv('Mouse_data.csv', index=False, quoting=csv.QUOTE_NONE)