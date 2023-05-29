import sys
sys.path.append("../")
import pandas as pd
import utilities.file_utilities as file_utilities


"""def data_extraction():
    l = []
    num_list = ['01', '03', '04', '05', '06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    for i in num_list:
        link = "https://secc.gov.in/getSCHhdSummaryDistrictReport.htm/33/{}".format(i)
        df = pd.read_html(link)
        l.append(df)
    return l

df = data_extraction()
raw_data = pd.concat([pd.DataFrame([container for i in df for container in i])], join='inner')
"""

df = pd.read_html("https://secc.gov.in/getSCHhdSummaryDistrictReport.htm/33/01")
raw_data = pd.DataFrame(df, columns=['District Name	Total Households', 'Landless households deriving major part of their income from manual casual labour', '%', 'Households with non-agricultural enterprises registered with government',	'%', 'Households paying income tax / professional tax','%', 'Households with Destitutes/living on alms	%	Households with salaried job in government	%	Households with salaried job in Public	%	Households with salaried job in Private'])

print(df)









