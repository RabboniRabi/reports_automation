"""
Module with function for G2C applications
"""


import sys
sys.path.append('../')


import utilities.utilities as utilities
import utilities.column_names_utilities as cols

import pandas as pd


def post_process_BRC_merge(raw_data):
    """
    Function to process the G2C application data at a school and converting them to the required configuration

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw G2C application data

    Returns:
    -------
    DataFrame object of G2C application data processed post mapping with BRC-CRC data
    """

    print('Post Processing before BRC merge called in CWSN')


    # Get school level wise total students count
    deo_wise_total_students_count = _get_grouping_level_wise_student_count (raw_data, initial_group_levels, cols.cwsn_name)

    # Get the school level wise count of students in school and in common pool
    school_wise_status_count = utilities.get_grouping_level_wise_col_values_count(
        raw_data, initial_group_levels, cols.cwsn_status, student_statuses)

    # Get block level wise count of valid student IDs
    school_wise_IDs_issued_count = _get_grouping_level_wise_IDs_issued_count(raw_data, initial_group_levels,\
         id_columns_regex_dict)    

    # Get the school level wise count of students with account
    school_wise_has_account_count = pd.pivot_table(raw_data, index=initial_group_levels, columns=cols.cwsn_has_acct,
                aggfunc='size', fill_value=0, sort=False).reset_index()


    # Merge the results into one school level summary
    df_data_schl_lvl = school_wise_total_students_count.merge(school_wise_status_count, on=initial_group_levels)
    df_data_schl_lvl = df_data_schl_lvl.merge(school_wise_IDs_issued_count, on=initial_group_levels)
    #df_data_schl_lvl = df_data_schl_lvl.merge(school_wise_has_account_count[initial_group_levels + [cols.yes_col, cols.no_col]])

    
    # Rename columns for better readability
    df_data_schl_lvl.rename(columns = {
        cols.cwsn_in_School : cols.stdnts_in_school,
        cols.cwsn_cp : cols.stdnts_in_cp,
        cols.nid : cols.nid_count,
        cols.udid : cols.udid_count}, inplace = True)

    return df_data_schl_lvl


