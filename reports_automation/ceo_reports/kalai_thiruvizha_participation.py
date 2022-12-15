"""
Module with functions to create Kalai Thiruvizha participation report for CEO review
- The report will rank data based on % of students that participated
"""

import sys
sys.path.append('../')

import pandas as pd
import os

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.report_utilities as report_utilities
import utilities.format_utilities as format_utilities
import utilities.column_names_utilities as cols

merge_dict = {
    'on_values' : [cols.district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
}

# Define the grouping levels for elementary report
elem_rep_group_level = [cols.district_name, cols.beo_user, cols.beo_name, \
cols.deo_name_elm, cols.school_category, cols.school_level]

# Define the grouping levels for secondary report
scnd_rep_group_level = [cols.district_name, cols.deo_name_sec, \
cols.school_category, cols.school_level]


# Build the arguments dictionary to do ranking for the report
ranking_args_dict = {
    'agg_dict': {
        cols.participants: 'sum', 
        cols.tot_students: 'sum'},
    'ranking_val_desc': cols.per_participants,
    'num_col': cols.participants,
    'den_col': cols.tot_students,
    'sort': True,
    'ascending': False
}

def _get_data_with_brc_mapping():
    """
    Function to fetch the Kalai Thiruvizha participation data, clean and  merge with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of Kalai Thiruvizha participation data updated with BRc-CRC mapping
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_data = dbutilities.fetch_data_as_df(credentials_dict, 'to_be_named.sql')

    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'kalai_thiruvizha_participants_count.xlsx')
    df_data = pd.read_excel(file_path, sheet_name='Report')

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_data, merge_dict)

    return data_with_brc_mapping

def get_kalai_vizha_particp_elementary_report(df_data = None):
    """
    Function to get the Kalai Thiruvizha participation elementary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The Kalai Thiruvizha participation data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of prepared elementary level Kalai Thiruvizha participation data
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Prepare the data for elementary report
    #data_grouped = df_data.groupby(elem_rep_group_level, as_index=False)[cols.participants, cols.tot_students].agg('sum')

    # Remove the line below and replace it with the line above when restoring BEO level reports
    data_grouped = df_data.groupby([cols.district_name, cols.deo_name_elm, cols.school_category, cols.school_level], as_index=False)[cols.participants, cols.tot_students].agg('sum')

    elem_report = report_utilities.get_elementary_report(data_grouped, 'percent_ranking', ranking_args_dict, 'KT', 'Attendance')                    

    return elem_report


def get_kalai_vizha_particp_secondary_report(df_data = None):
    """
    Function to get the Kalai Thiruvizha participation secondary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The Kalai Thiruvizha participation data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of prepared secondary level Kalai Thiruvizha participation data
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]

    # Prepare the data for secondary report
    data_grouped = df_data.groupby(scnd_rep_group_level, as_index=False)[cols.participants, cols.tot_students].agg('sum')

    secnd_report = report_utilities.get_secondary_report(data_grouped, 'percent_ranking', ranking_args_dict, 'KT', 'Attendance')                    

    return secnd_report



def run():
    """
    Function to call other internal functions and create the Kalai Thiruvizha participation reports
    """

    # Get the Kalai Thiruvizha data updated with BRC mapping
    data_with_brc_mapping = _get_data_with_brc_mapping()

    # Get the elementary report
    elem_report = get_kalai_vizha_particp_elementary_report(data_with_brc_mapping.copy())

    # Get the secondary report
    secnd_report = get_kalai_vizha_particp_secondary_report(data_with_brc_mapping.copy())

    format_utilities.format_col_to_percent_and_save(elem_report, cols.per_participants, 'Kalai Thiruvizha Elementary',
            'Kalai Thiruvizha participation Elementary Report.xlsx', dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())   

    format_utilities.format_col_to_percent_and_save(secnd_report, cols.per_participants, 'Kalai Thiruvizha Secondary',
            'Kalai Thiruvizha participation Secondary Report.xlsx', dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())   


if __name__ == "__main__":
    run()
