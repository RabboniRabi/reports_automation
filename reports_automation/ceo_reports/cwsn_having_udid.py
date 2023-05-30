"""
Module with function for custom pre-processing of CWSN raw data
"""


import sys
sys.path.append('../')


import utilities.utilities as utilities
import utilities.column_names_utilities as cols

import pandas as pd

# Define the initial grouping level
initial_group_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.school_category]

# Define list of student statuses to count in report
student_statuses = [cols.cwsn_in_School, cols.cwsn_cp]

# Define regex of ID values to accept
id_columns_regex_dict = {
    # Accept only 5 digit numbers or vales starting with TN and ends with range of 3 to 6 digits.
        cols.nid : '(?i)(^[0-9]{5,6}$)|(^TN[\s\S][a-z]{2,5}[\s\S][a-z]{2,5}[\s\S][0-9]{3,6}$)|(^TN[\s\S][a-z]{2,5}[\s\S][a-z]{2,5}[\s\S][0-9]{3,6}[\s\S][0-9]{2,4}$)',
        cols.udid: '(?i)^TN.*$'  # Accept only values starting with TN
    }

def _get_grouping_level_wise_IDs_issued_count(df, group_levels, columns_regex_dict):
    """
    Internal function to get the grouping levels wise count of students with disability IDs.

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    columns_regex_dict: dict
        A column - regex of accepted values key - value pair dictionary
        This dictionary will be used to filter values in the ID columns by matching only the values
        given in the regex
        eg: {
            'col_a' : '[1-9].',
            'col_b' : '(a|h|e)+
        }           
    Returns:
    --------
    DataFrame object with group level wise count of students with disability ids
    """
    # Drop missing values in IDs
    df = df.dropna(subset=columns_regex_dict.keys())

    df_filtered_grouped = utilities.filter_group_count_valid_values(df, group_levels, columns_regex_dict)

    # The union of regexes would mean that some cells in a row have no regex matches count
    # while other cells in the same row do. This would mean some cells are NAs.
    # Replace those NA cells with 0s.
    df_filtered_grouped.fillna(0, inplace=True)

    return df_filtered_grouped

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

    df_grouped = df.groupby(group_levels,sort=False)[student_count_col].count().reset_index()

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

    # Filtering the raw data only for In school students
    raw_data = raw_data[raw_data[cols.cwsn_status] == cols.cwsn_in_School]

    # As the raw data is at student level, group the data to school level and count values needed for report

    # Get school level wise total students count
    school_wise_total_students_count = _get_grouping_level_wise_student_count (raw_data, initial_group_levels, cols.cwsn_name)

    # Get the school level wise count of students in school and in common pool
    #school_wise_status_count = utilities.get_grouping_level_wise_col_values_count(
        #raw_data, initial_group_levels, cols.cwsn_status, student_statuses)

    # Get block level wise count of valid student IDs
    school_wise_IDs_issued_count = _get_grouping_level_wise_IDs_issued_count(raw_data, initial_group_levels,\
         id_columns_regex_dict)    

    # Get the school level wise count of students with account
    school_wise_has_account_count = pd.pivot_table(raw_data, index=initial_group_levels, columns=cols.cwsn_has_acct,
                aggfunc='size', fill_value=0, sort=False).reset_index()


    # Merge the results into one school level summary
    df_data_schl_lvl = school_wise_total_students_count.merge(school_wise_IDs_issued_count, on=initial_group_levels, how='left')
    #df_data_schl_lvl = df_data_schl_lvl.merge(school_wise_IDs_issued_count, on=initial_group_levels, how='left')
    #df_data_schl_lvl = df_data_schl_lvl.merge(school_wise_has_account_count[initial_group_levels + [cols.yes_col, cols.no_col]], how='left')

    
    # Rename columns for better readability
    df_data_schl_lvl.rename(columns = {
        cols.cwsn_in_School : cols.stdnts_in_school,
        cols.cwsn_cp : cols.stdnts_in_cp,
        cols.nid : cols.nid_count,
        cols.udid : cols.udid_count}, inplace = True)

    return df_data_schl_lvl


