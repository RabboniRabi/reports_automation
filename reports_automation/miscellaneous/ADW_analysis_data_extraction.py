import sys
sys.path.append("../")
import pandas as pd
import numpy as np
import utilities.file_utilities as file_utilities



"""df_list = pd.read_html("https://secc.gov.in/getSCCategoryIncomeSlabStateReport.htm/33")
df = df_list[0]
print(df)
print('type of first list object: ', type(df))
file_utilities.save_to_excel({'test_data_extraction':df}, 'test_data_extraction.xlsx', index=True)

print(df)

"""



def data_extraction():
    """
    Function to traverse through different District's link and extract the tehsil data.

    Returns:
    -------
    DataFrame object of each District's Tehsil data

    """
    # Creating an empty dataframe for storing every district's tehsil information
    data = pd.DataFrame()
    # Loop to extract tehsil level information
    for i in range(1, 34):
        try:
            #Till i=9 the html link starts from 0
            if i < 10:
                link = "https://secc.gov.in/getSCHhdSummaryDistrictReport.htm/33/0{}".format(i)
                df_list = pd.read_html(link) # try catch for 404. If 404, go to next i
                df = df_list[0]
                data = pd.concat([data, df])
            else:
                link = "https://secc.gov.in/getSCHhdSummaryDistrictReport.htm/33/{}".format(i)
                df_list = pd.read_html(link)  # try catch for 404. If 404, go to next i
                df = df_list[0]
                data = pd.concat([data, df])
        except ValueError:
            # If there is a value error, the loop goes to the next iteration.
            continue
    return data
"""def get_district_name_from_index(index):

    return district_name

"""
extracted_data = data_extraction()
# Saving the extracted data in the excel file.
file_utilities.save_to_excel({'test_data_extraction': extracted_data}, 'test_data_extraction3.xlsx', index=True)









