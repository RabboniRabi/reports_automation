import sys
sys.path.append('../')
import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import utilities.file_utilities as file_utilities
import numpy as np
# Define the levels to group the data by
grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, "Management", "Sub_Management"]
agg_dict = {
    "total_marks": "sum",
    "No_of_Students_Enrolled": "count",
    "subj1_centum": "sum",
    "subj2_centum": "sum",
    "subj3_centum": "sum",
    "subj4_centum": "sum",
    "subj5_centum": "sum",
    "Pass" : 'sum',
    "average_marks": "mean",
    'Between 35% to 60%': "sum",
    "Between 60% to 80%": "sum",
    '80% and above': "sum"
}

sc_agg_dict = {
    "emis_id": "count",
    "Pass" : 'sum'
}

def total_marks_summary_schoolwise():
    """

    Args:
        raw_data:

    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the 10th board exam marks from the database as a Pandas DataFrame object
    raw_data = dbutilities.fetch_data_as_df(credentials_dict, 'sslc_student_marks.sql')
    # Rename the column names to standard format
    raw_data = column_cleaner.standardise_column_names(raw_data)
    raw_data.rename(columns={
        "emis_id": "No_of_Students_Enrolled"
    }, inplace=True)
    print(raw_data.columns)
    raw_data['total_marks'].replace(to_replace="AAA", value=0, inplace=True)
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
    raw_data['average_marks'] = raw_data['total_marks']/5
    pass_and_less_than_60_condition = [
        (raw_data['average_marks'] < 60) & (raw_data['Pass'])
    ]
    between_60_and_80_condition = [
        ((raw_data['average_marks'] >= 60) & (raw_data['average_marks'] < 80 ) & (raw_data['Pass']))
    ]
    above_80_condition = [
        ((raw_data['average_marks'] >= 80) & (raw_data['Pass']))
    ]
    choices = [1]
    raw_data['Between 35% to 60%'] = np.select(pass_and_less_than_60_condition,choices, default=0)
    raw_data['Between 60% to 80%'] = np.select(between_60_and_80_condition,choices, default=0)
    raw_data['80% and above'] = np.select(above_80_condition,choices, default=0)
    # Group the data to grouping_level
    df_data_grouped = raw_data.groupby(grouping_levels, as_index=False).agg(agg_dict)
    df_data_grouped['Pass %'] = (df_data_grouped['Pass'] / df_data_grouped['No_of_Students_Enrolled'])
    file_utilities.save_to_excel({'sslc_student_marks': df_data_grouped}, 'sslc_student_marks_.xlsx', index=True)


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
    raw_data['total_marks'].replace(to_replace="AAA", value=0, inplace=True)
    # Convert all column types to string
    raw_data = raw_data.astype({
        "total_marks": "int",
        "subj1_centum": "int",
        "subj2_centum": "int",
        "subj3_centum": "int",
        "subj4_centum": "int",
        "subj5_centum": "int",
        })
    # print(raw_data.columns)
    raw_data['average_marks'] = raw_data['total_marks']/5
    
    # Group the data to grouping_level
    df_data_grouped = raw_data.groupby(['community', 'Sub_Management'], as_index=False).agg(sc_agg_dict)

    print(df_data_grouped)
    file_utilities.save_to_excel({'sslc_sc_student_marks': df_data_grouped}, 'sslc_sc_student_marks.xlsx', index=True)



sc_students_marks_summary()