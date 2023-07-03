import sys
sys.path.append('../')
import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import utilities.file_utilities as file_utilities
import numpy as np
# Define the levels to group the data by
grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name,"dpi","management"]
agg_dict = {
    "total_marks": "sum",
    "emis_id": "count",
    "subj1_centum": "sum",
    "subj2_centum": "sum",
    "subj3_centum": "sum",
    "subj4_centum": "sum",
    "subj5_centum": "sum",
    "pass": 'sum',
    "average_marks": "mean",
    'Between 35% to 60%': "sum",
    "Between 60% to 80%": "sum",
    '80% and above': "sum",
    "Major Groups": "sum",
    "Vocational Groups": "sum"
}

sc_agg_dict = {
    "emis_id": "count",
    "pass" : 'sum'
}

def total_marks_summary_schoolwise():
    """

    Function to w

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials_rabboni.json')

    # Get the common pool to be surveyed details from the database as a Pandas DataFrame object
    raw_data = dbutilities.fetch_data_as_df(credentials_dict, 'hsc_student_marks.sql')
    file_utilities.save_to_excel({'hsc_student_marks_schoolwise': raw_data}, 'hsc_student_marks.xlsx', index=True)

total_marks_summary_schoolwise()