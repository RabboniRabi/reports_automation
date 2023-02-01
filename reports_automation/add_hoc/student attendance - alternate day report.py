import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols

import pandas as pd
import numpy as np

# Read the database connection credentials
credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

# Get the latest students and teachers count
df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_attendance_masterfile.sql')

print(df_report)








