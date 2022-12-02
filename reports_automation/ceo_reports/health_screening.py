"""
Module with functions to create health screening report for CEO reports.
This module contains functions to create reports for:
- Health screening students completed
- Health screening schools completed
"""

import os
import sys
sys.path.append('../')


import pandas as pd

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.report_utilities as report_utilities
import utilities.column_names_utilities as cols

merge_dict = {
    'on_values' : [cols.district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
}

# Define the grouping levels for elementary report
elem_rep_group_level = [cols.district_name, cols.block_name, cols.beo_user, cols.beo_name, \
cols.deo_name_elm, cols.school_category, cols.school_level]

# Define the grouping levels for secondary report
scnd_rep_group_level = [cols.district_name, cols.block_name, cols.deo_name_sec, \
cols.school_category, cols.school_level]

# Build the arguments dictionary to do ranking for the report
ranking_args_dict = {
    'agg_cols': [cols.total, cols.screened],
    'agg_func': 'sum',
    'ranking_val_desc': '% Screened',
    'num_col': cols.screened,
    'den_col': cols.total,
    'sort': True,
    'ascending': False
}


def get_data_with_brc_mapping():
    """
    Function to fetch the health data merged with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of health data updated with BRc-CRC mapping
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'health_screening_status.sql')

    # Save the fetched data for reference
    #file_utilities.save_to_excel({'Report': df_report}, 'health_screening_status.xlsx', dir_path = file_utilities.get_source_data_dir_path())

    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'health_screening_status.xlsx')
    df_report = pd.read_excel(file_path)

    #print('df_report: ', df_report)

    #print('df_report columns: ', df_report.columns.to_list())

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_report, merge_dict)

    # Intermediate saves to test each save
    file_utilities.save_to_excel({'Test': data_with_brc_mapping}, 'data_with_brc_mapping_health.xlsx')

    return data_with_brc_mapping


def get_students_elementary_health_report():
    """
    Function to fetch the elementary health report of studentss
    
    Returns:
    -------
    DataFrame object of elementary students' health report
    """

    # Get the BRC-CRC mapped health data
    df_data = get_data_with_brc_mapping()

    # Group the data for elementary and secondary reports generation
    data_for_elem = data_with_brc_mapping.groupby(elem_rep_group_level, as_index=False)[cols.screened, cols.total].agg('sum')

    # Get the Elementary report
    elem_report = report_utilities.get_elementary_report(\
        data_for_elem, 'percent_ranking', ranking_args_dict, 'HC', 'Health')

    return elem_report


def get_students_secondary_health_report():
    """
    Function to fetch the elementary health report of studentss
    
    Returns:
    -------
    DataFrame object of secondary students' health report
    """
    data_for_secnd = data_with_brc_mapping.groupby(scnd_rep_group_level, as_index=False)[cols.screened, cols.total].agg('sum')

    # Get the Secondary report
    secnd_report = report_utilities.get_secondary_report(\
        data_for_secnd, 'percent_ranking', ranking_args_dict, 'HC', 'Health')

    return secnd_report



def update_data_with_school_level_scrn_count():
    """
    Function to update the data with school level
    Fully completed, Partially Completed, 'Not Started' screening statuses.
    """    



def run():
    """
    Function to call other internal functions and create the Health screening status reports
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'health_screening_status.sql')

    # Save the fetched data for reference
    #file_utilities.save_to_excel({'Report': df_report}, 'health_screening_status.xlsx', dir_path = file_utilities.get_source_data_dir_path())

    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'health_screening_status.xlsx')
    df_report = pd.read_excel(file_path)

    #print('df_report: ', df_report)

    #print('df_report columns: ', df_report.columns.to_list())

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_report, merge_dict)

    # Intermediate saves to test each save
    file_utilities.save_to_excel({'Test': data_with_brc_mapping}, 'data_with_brc_mapping_health.xlsx')



    # Group the data for elementary and secondary reports generation
    data_for_elem = data_with_brc_mapping.groupby(elem_rep_group_level, as_index=False)[cols.screened, cols.total].agg('sum')
    data_for_secnd = data_with_brc_mapping.groupby(scnd_rep_group_level, as_index=False)[cols.screened, cols.total].agg('sum')

    # Intermediate saves to test each save
    file_utilities.save_to_excel({'Test': data_for_elem}, 'Test_health.xlsx')

    # Get the Elementary report
    elem_report = report_utilities.get_elementary_report(\
        data_for_elem, 'percent_ranking', ranking_args_dict, 'HC', 'Health')

    # Save the elementary report
    file_utilities.save_to_excel({'Health Report (Elementary)': elem_report}, 'Health Report.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())

    # Get the Secondary report
    secnd_report = report_utilities.get_secondary_report(\
        data_for_secnd, 'percent_ranking', ranking_args_dict, 'HC', 'Health')

    # Save the secondary report
    file_utilities.save_to_excel({'Health Report (Secondary)': secnd_report}, 'Health Report.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())         




if __name__ == "__main__":
    run()
