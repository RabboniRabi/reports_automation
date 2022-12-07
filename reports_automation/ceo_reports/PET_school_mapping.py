"""
Module to functions to create PET to School mapping report for CEO review
- The report will rank data based on % of schools that have fully completed mapping
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

# Define elementary indexes for pivoting
elem_pivot_index = [cols.district_name, cols.deo_name_elm, cols.school_category]
# Define secondary indexes for pivoting
scnd_pivot_index = [cols.district_name, cols.deo_name_sec, cols.school_category]

merge_dict = {
    'on_values' : [cols.district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
}

# Build the arguments dictionary to do ranking for the report
ranking_args_dict = {
    'agg_dict': {
        cols.fully_mapped: 'sum', 
        cols.part_mapped: 'sum',
        cols.tot_schools: 'sum'},
    'ranking_val_desc': cols.perc_fully_mapped,
    'num_col': cols.fully_mapped,
    'den_col': cols.tot_schools,
    'sort': True,
    'ascending': False
}

def _get_data_with_brc_mapping():
    """
    Function to fetch the Commpon Pool data, clean and  merge with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of Common Pool data updated with BRc-CRC mapping
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_data = dbutilities.fetch_data_as_df(credentials_dict, 'tpd_attendance.sql')

    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'Pet-to-school-Mapping-Rpt.xlsx')
    df_data = pd.read_excel(file_path, sheet_name='Report', skiprows=4)

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_data, merge_dict)

    return data_with_brc_mapping


def _process_data_for_report(df_data, pivot_index):
    """
    Internal function to get a report ready data by:
        - Pivoting and getting mapped statuses count of schools at grouping level
        - Total count of schools at grouping level
    """
    # Pivot the table on mapping status
    df_data_pivot = pd.pivot_table(df_data, values=cols.school_name, \
                        index=pivot_index ,columns=[cols.mapping_status], aggfunc='count',fill_value=0).reset_index()

    # Update with the total ageing data
    df_data_pivot[cols.tot_schools] = df_data_pivot[[cols.fully_mapped, cols.part_mapped]].sum(axis=1)

    return df_data_pivot                    



def get_pet_mapping_elementary_report(df_data = None):
    """
    Function to get the PET to school mapping elementary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The PET to school mapping data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of prepared elementary level PET to school mapping data
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Prepare the data for elementary report
    elem_processed_data = _process_data_for_report(df_data, elem_pivot_index)

    elem_report = report_utilities.get_elementary_report(elem_processed_data, 'percent_ranking', ranking_args_dict, 'PET', 'Operations')                    

    return elem_report

def get_pet_mapping_secondary_report(df_data = None):
    """
    Function to get the PET to school mapping secondary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The PET to school mapping data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of prepared secondary level PET to school mapping data
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()    

    # Filter the data to Secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]    

    # Prepare the data for secondary report
    secnd_processed_data = _process_data_for_report(df_data, scnd_pivot_index)

    # Get the Secondary report
    secnd_report = report_utilities.get_secondary_report(secnd_processed_data, 'percent_ranking', ranking_args_dict, 'PET', 'Operations')

    return secnd_report
    

def run():
    """
    Function to call other internal functions and create the Common Pool reports
    """

    # Get the Commpon Pool data updated with BRC mapping
    data_with_brc_mapping = _get_data_with_brc_mapping()

    # Get the elementary report
    elem_report = get_pet_mapping_elementary_report(data_with_brc_mapping.copy())

    # Get the secondary report
    secnd_report = get_pet_mapping_secondary_report(data_with_brc_mapping.copy())

    # Save the elementary report
    """file_utilities.save_to_excel({'PET Mapping Elementary Report' : elem_report}, 'PET Mapping Elementary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())"""

    format_utilities.format_col_to_percent_and_save(elem_report, cols.perc_fully_mapped, 'PET Mapping Elementary Report',
            'PET Mapping Elementary Report.xlsx', dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())   

    # Save the secondary report
    """file_utilities.save_to_excel({'PET Mapping Secondary Report' : secnd_report}, 'PET Mapping Secondary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path()) """

    format_utilities.format_col_to_percent_and_save(secnd_report, cols.perc_fully_mapped, 'PET Mapping Secondary Report',
            'PET Mapping Secondary Report.xlsx', dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())   

if __name__ == "__main__":
    run()
