import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols

import pandas as pd
import numpy as np

Total_Schools = "school_name"


working_schools = 'partial_yn'
working_status = ["1","2"]
groupby_index = ['district_name']
#grouping_cols = ['disctict_name', 'marked', 'partially_marked', ]
groupby_criteria = {"marked":"sum","partially_marked":"sum","unmarked":"sum",Total_Schools:"count"}

# Read the database connection credentials
credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

# Get the latest students and teachers count
df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_attendance_masterfile.sql')

#consider only the fully and partially working schools (yn is either 1 or 2) using isin.
df_filtered = utilities.filter_dataframe_not_in_column(df_report,working_schools,working_status)

#groupby district - keep this variable to add block if necessary - and sum marked,partially marked and unmarked and % calc
df_filtered = df_filtered.groupby(groupby_index).agg(groupby_criteria)
df_filtered['% Marked Schools'],df_filtered['% Unmarked Schools'] =  df_filtered['marked']/df_filtered[Total_Schools],\
                                                                     df_filtered['unmarked']/df_filtered[Total_Schools]

#sortby highest unmarked
df_filtered.sort_values(['% Unmarked Schools'],ascending=False)

print(df_filtered)








