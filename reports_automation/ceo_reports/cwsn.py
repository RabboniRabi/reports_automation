"""
Module with functions to create CWSN reports for CEO reports.
This module contains functions to create reports for:
    - UDID numbers
    - Accounts
"""

import os
import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.report_utilities as report_utilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols

import pandas as pd

# Define the initial grouping level
initial_group_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.school_category]

# Define list of student statuses to count in report
student_statuses = [cols.cwsn_in_School, cols.cwsn_cp]

# Define regex of ID values to accept
id_columns_regex_dict = {
        'NID' : '^[0-9]{5}$', # Accept only 5 digit numbers
        'UDID': 'TN.'  # Accept only values starting with TN
    }

merge_dict = {
    'on_values' : [cols.district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
}

# Define the grouping levels for elementary report
elem_rep_group_level = [cols.district_name, cols.block_name, cols.beo_user, cols.beo_name, \
cols.deo_name_elm, cols.school_category, cols.school_level]

# Define the grouping levels for secondary report
scnd_rep_group_level = [cols.district_name, cols.deo_name_sec, \
cols.school_category, cols.school_level]

# Build the arguments dictionary to do ranking for the report
agg_dict = {
        cols.cwsn_tot: 'sum', 
        cols.stdnts_in_school: 'sum', 
        cols.stdnts_in_cp : 'sum',
        cols.nid_count : 'sum',
        cols.udid_count : 'sum',
        cols.with_acct: 'sum',
        cols.witht_acct : 'sum'
    }
ranking_args_dict = {
    'agg_dict': agg_dict,
    'ranking_val_desc': '% Students with UDID',
    'num_col': cols.udid_count,
    'den_col': cols.cwsn_tot,
    'sort': True,
    'ascending': False
}


def _get_grouping_level_wise_IDs_issued_count(df, group_levels, columns_regex_dict):
    """
    Function to get the grouping levels wise count of students with disability IDs.

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

    return df_filtered_grouped

def _get_grouping_level_wise_student_count(df, group_levels, student_count_col):
    """
    Function to get the grouping levels wise count of CWSN students

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

def _get_data_with_brc_mapping():
    """
    Function to fetch the CWSN data merged with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of CWSN data updated with BRc-CRC mapping
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'to_be_filled.sql')


    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'CWSN-Report.xlsx')
    df_report = pd.read_excel(file_path, sheet_name='Report', skiprows=4)

    # As the data is at student level, group the data to school level and count values needed for report

    # Get school level wise total students count
    school_wise_total_students_count = _get_grouping_level_wise_student_count (df_report, initial_group_levels, cols.cwsn_name)

    # Get the school level wise count of students in school and in common pool
    school_wise_status_count = utilities.get_grouping_level_wise_col_values_count(
        df_report, initial_group_levels, cols.cwsn_status, student_statuses)

    # Get block level wise count of valid student IDs
    school_wise_IDs_issued_count = _get_grouping_level_wise_IDs_issued_count(df_report, initial_group_levels,\
         id_columns_regex_dict)    

    # Get the school level wise count of students with account
    school_wise_has_account_count = pd.pivot_table(df_report, index=initial_group_levels, columns=cols.cwsn_has_acct,
                aggfunc='size', fill_value=0, sort=False).reset_index()


    # Merge the results into one school level summary
    df_data_schl_lvl = school_wise_total_students_count.merge(school_wise_status_count[initial_group_levels+student_statuses])
    df_data_schl_lvl = df_data_schl_lvl.merge(school_wise_IDs_issued_count[initial_group_levels+[cols.nid, cols.udid]])
    df_data_schl_lvl = df_data_schl_lvl.merge(school_wise_has_account_count[initial_group_levels + [cols.yes_col, cols.no_col]])

    
    # Rename columns for better readability
    df_data_schl_lvl.rename(columns = {
        cols.cwsn_in_School : cols.stdnts_in_school,
        cols.cwsn_cp : cols.stdnts_in_cp,
        cols.nid : cols.nid_count,
        cols.udid : cols.udid_count,
        cols.yes_col : cols.with_acct,
        cols.no_col : cols.witht_acct
        }, inplace = True)

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_data_schl_lvl, merge_dict)

    return data_with_brc_mapping



def get_cwsn_elementary_report(df_data = None):
    """
    Function to get the CWSN elementary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The school level CWSN data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of elementary students' CWSN report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Group the data to school category level for elementary reports generation
    #data_for_elem = df_data.groupby(elem_rep_group_level, as_index=False).agg(agg_dict)

    # Replace the line below with the line above when restoring BEO level ranking
    data_for_elem = df_data.groupby([cols.district_name, cols.deo_name_elm, cols.school_category, cols.school_level], as_index=False).agg(agg_dict)

    # Get the Elementary report
    elem_report = report_utilities.get_elementary_report(\
        data_for_elem, 'percent_ranking', ranking_args_dict, 'CWSN', 'Data Quality')

    return elem_report    

def get_cwsn_secondary_report(df_data = None):
    """
    Function to get the CWSN secondary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The school level CWSN data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of secondary students' CWSN report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()    

    # Filter the data to Secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]    

    # Group the data to school category level for secondary reports generation
    data_for_secnd = df_data.groupby(scnd_rep_group_level, as_index=False).agg(agg_dict)

    # Get the Secondary report
    secnd_report = report_utilities.get_secondary_report(\
        data_for_secnd, 'percent_ranking', ranking_args_dict, 'CWSN', 'Data Quality')

    return secnd_report
    


def run():
    """
    Function to call other internal functions and create the Health screening status reports
    """

    # Get the CWSN data updated with BRC mapping
    data_with_brc_mapping = _get_data_with_brc_mapping()

    # Get the elementary report
    elem_report = get_cwsn_elementary_report(data_with_brc_mapping.copy())

    # Get the secondary report
    secnd_report = get_cwsn_secondary_report(data_with_brc_mapping.copy())

    # Save the elementary report
    file_utilities.save_to_excel({'CWSN Elementary Report' : elem_report}, 'CWSN Elementary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())   

    # Save the secondary report
    file_utilities.save_to_excel({'CWSN Secondary Report' : secnd_report}, 'CWSN Secondary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())   


if __name__ == "__main__":
    run()
