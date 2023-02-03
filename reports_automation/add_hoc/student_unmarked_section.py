from datetime import datetime
from datetime import timedelta
import imgkit
import sys

sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols
import openpyxl
import dataframe_image as dfi


from openpyxl.styles import Color,Font, Alignment, Border, Side, PatternFill,fills

from openpyxl.styles import colors
from openpyxl.cell import Cell

import pandas as pd

Total_Schools = "school_name"
groupby_index = ['district_name']
groupby_criteria = {"udise_code":"count"}

# Read the database connection credentials
credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

# Get the latest students and teachers count
df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_unmarked_weekly.sql')
df_sections = dbutilities.fetch_data_as_df(credentials_dict, 'total_sections.sql')



#groupby district - keep this variable to add block if necessary - and sum marked,partially marked and unmarked and % calc
df_filtered = df_report.groupby(groupby_index).agg(groupby_criteria).reset_index()

df_filtered = pd.merge(df_filtered,df_sections,on=['district_name'])

df_filtered.rename(columns={'district_name':'District',"count(section)":"Total Sections"},
                                inplace=True)
#sortby highest unmarked

function_dict = {"Total Sections":"sum","udise_code":"sum"}
df_filtered.loc[-1,:] = df_filtered.aggregate(function_dict)

df_filtered.at[-1, 'District'] = "Grand Total"

datatoexcel = pd.ExcelWriter(r'C:\Users\Admin\Downloads\unmarkedtest.xlsx', engine='xlsxwriter')

df_filtered.to_excel(datatoexcel, sheet_name='School unMarking',index=False)
# save the excel
datatoexcel.save()
