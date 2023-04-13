"""
Module with function for custom pre-processing of CWSN raw data
for CWSN students with bank account report
"""


import sys
sys.path.append('../')


import utilities.utilities as utilities
import utilities.column_names_utilities as cols

import pandas as pd

# Define the initial grouping level
initial_group_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.school_category]


def _get_grouping_level_wise_student_count(df, group_levels, student_count_col):
    """
    Internal function to get the grouping levels wise count of CWSN students

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    student_count_col: str
        The column to count
    Returns:
    --------
    DataFrame object with group level wise count of total CWSN students
    """

    df_grouped = df.groupby(group_levels, sort=False)[student_count_col].count().reset_index()

    df_grouped.rename(columns={student_count_col: cols.cwsn_tot}, inplace=True)

    return df_grouped    

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

    print('Pre Processing before BRC merge called in CWSN')

    # As the raw data is at student level, group the data to school level and count values needed for report

    # Get school level wise total students count
    school_wise_total_students_count = _get_grouping_level_wise_student_count (raw_data, initial_group_levels, cols.cwsn_name)

    # Get the school level wise count of students with account
    school_wise_has_account_count = pd.pivot_table(raw_data, index=initial_group_levels, columns=cols.cwsn_has_acct,
                aggfunc='size', fill_value=0, sort=False).reset_index()


    # Merge the results into one school level summary
    df_data_schl_lvl = school_wise_total_students_count.merge(school_wise_has_account_count, on=initial_group_levels, how='left')

    
    # Rename columns for better readability
    df_data_schl_lvl.rename(columns = {
        cols.cwsn_in_School : cols.stdnts_in_school,
        cols.yes_col : cols.with_acct,
        cols.no_col : cols.witht_acct
        }, inplace = True)

    return df_data_schl_lvl


