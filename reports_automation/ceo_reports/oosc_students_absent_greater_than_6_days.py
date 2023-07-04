"""
Module with function for custom pre-processing of OoSC Students absent greater than 6 days report
"""

import sys
sys.path.append('../')
import utilities.file_utilities as file_utilities

import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import pandas as pd


# Define the initial grouping level
initial_group_levels = [cols.block_name, cols.udise_col, cols.school_name]

def pre_process_BRC_merge(raw_data):
    """
    Function to process the CWSN raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw CWSN data

    Returns:
    -------
    DataFrame object of CWSN data processed and ready for mapping with BRC-CRC data
    """

    print('Pre Processing before BRC merge called in Oosc students greater than 6 days report')

    # Rename the column names to standard format
    column_cleaner.standardise_column_names(raw_data)

    # Get the number of students absent for greater than 6 days at the initial grouping level
    df_pre_processed = raw_data.groupby(initial_group_levels)[cols.oosc_stu_id].count().reset_index()

    # Rename columns
    df_pre_processed.rename(columns={cols.oosc_stu_id: cols.oosc_no_stu_absent_greater_6}, inplace=True)

    return df_pre_processed
