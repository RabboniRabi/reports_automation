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
    "pass" : 'sum',
    "average_marks": "mean",
    'Between 35% to 60%': "sum",
    "Between 60% to 80%": "sum",
    '80% and above': "sum"
}

sc_agg_dict = {
    "emis_id": "count",
    "pass" : 'sum'
}

def total_marks_summary_schoolwise():
    """

    Args:
        raw_data:

    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the common pool to be surveyed details from the database as a Pandas DataFrame object
    raw_data = dbutilities.fetch_data_as_df(credentials_dict, 'sslc_student_marks.sql')
    # Rename the column names to standard format
    raw_data = column_cleaner.standardise_column_names(raw_data)
    raw_data['total_marks'].replace(to_replace="AAA", value="11111", inplace=True)
    raw_data['total_marks'].replace(to_replace=" ", value="22222", inplace=True)
    # Convert all column types to string
    raw_data = raw_data.astype({
        "total_marks": "int",
        "subj1_centum": "int",
        "subj2_centum": "int",
        "subj3_centum": "int",
        "subj4_centum": "int",
        "subj5_centum": "int"
        })
    print(raw_data.columns)
    raw_data['average_marks'] = raw_data['total_marks']/500
    pass_and_less_than_60_condition = [
        (raw_data['average_marks'] < .6) & (raw_data['Pass'])
    ]
    between_60_and_80_condition = [
        ((raw_data['average_marks'] >= .6) & (raw_data['average_marks'] < .8 ) & (raw_data['pass']))
    ]
    above_80_condition = [
        ((raw_data['average_marks'] >= .8) & (raw_data['pass']))
    ]
    choices = [1]
    raw_data['Between 35% to 60%'] = np.select(pass_and_less_than_60_condition,choices, default=0)
    raw_data['Between 60% to 80%'] = np.select(between_60_and_80_condition,choices, default=0)
    raw_data['80% and above'] = np.select(above_80_condition,choices, default=0)
    # Group the data to grouping_level
    df_data_grouped = raw_data.groupby(grouping_levels, as_index=False).agg(agg_dict)
    file_utilities.save_to_excel({'sslc_student_marks': df_data_grouped}, 'sslc_student_marks.xlsx', index=True)


def sc_students_marks_summary():
    """

    Args:
        raw_data:

    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the common pool to be surveyed details from the database as a Pandas DataFrame object
    raw_data = dbutilities.fetch_data_as_df(credentials_dict, 'sslc_sc_student_marks.sql')
    # Rename the column names to standard format
    raw_data = column_cleaner.standardise_column_names(raw_data)
    # Convert all column types to string
    raw_data = raw_data.astype({
        "total_marks": "int",
        "subj1_centum": "int",
        "subj2_centum": "int",
        "subj3_centum": "int",
        "subj4_centum": "int",
        "subj5_centum": "int",
        "subj1_pass": "int",
        "subj2_pass": "int",
        "subj3_pass": "int",
        "subj4_pass": "int",
        "subj5_pass": "int"
        })
    #print(raw_data.columns)
    raw_data['pass'] = (raw_data['subj1_pass'] + raw_data['subj2_pass'] + raw_data['subj3_pass'] + raw_data['subj4_pass'] + raw_data['subj5_pass'] == 5)
    raw_data['average_marks'] = raw_data['total_marks']/500
    
    # Group the data to grouping_level
    df_data_grouped = raw_data.groupby(['school_management_type'], as_index=False).agg(sc_agg_dict)
    print(df_data_grouped)
    #file_utilities.save_to_excel({'sslc_sc_student_marks': df_data_grouped}, 'sslc_sc_student_marks.xlsx', index=True)



total_marks_summary_schoolwise()