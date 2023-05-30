import sys
sys.path.append("../")
import pandas as pd
import numpy as np
import utilities.file_utilities as file_utilities



df_list = pd.read_html("https://secc.gov.in/getSCCategoryIncomeSlabStateReport.htm/33")
df = df_list[0]
print(df)
print('type of first list object: ', type(df))
file_utilities.save_to_excel({'test_data_extraction':df}, 'test_data_extraction.xlsx', index=True)
#raw_data = pd.DataFrame(df, columns=['District Name	Total Households', 'Landless households deriving major part of their income from manual casual labour', '%', 'Households with non-agricultural enterprises registered with government',	'%', 'Households paying income tax / professional tax','%', 'Households with Destitutes/living on alms	%	Households with salaried job in government	%	Households with salaried job in Public	%	Households with salaried job in Private'])

print(df)



"""

def data_extraction():

########### Try something like this
    for i in range (1,35):
        link = "https://secc.gov.in/getSCHhdSummaryDistrictReport.htm/33/{}".format(i)
        df = pd.read_html(link) # try catch for 404. If 404, go to next i
        l.append(df)
    return l

df = data_extraction()
raw_data = pd.concat([pd.DataFrame([container for i in df for container in i])], join='inner')
"""








