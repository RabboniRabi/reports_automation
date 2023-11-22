"""
Module with custom functions to add Total students count in students attendance report.
"""

import sys

sys.path.append('../')

import utilities.column_names_utilities as cols

import pandas as pd

import utilities.dbutilities as dbutilities

# Define grouping levels
grouping_level = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name]


def pre_process_BRC_merge(raw_data: pd.DataFrame):
    """
    Function to process the Total students raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw potential dropouts

    Returns:
    -------
    DataFrame object of Total students data processed and ready for mapping with BRC-CRC data
    """


    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
    df_total_students_count = dbutilities.fetch_data_as_df(credentials_dict,
                                                           'total_students_count.sql')

    # Merge the total students count to the raw data
    df_merged = pd.merge(df_total_students_count, raw_data, on=grouping_level, how='left')

    return df_merged
