"""
Module with functions to:
- Create the TPD training attendance report for the CEO review report.

"""

import sys
sys.path.append('../')

import pandas as pd
import os

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.report_utilities as report_utilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner

merge_dict = {
    'on_values' : [cols.district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
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
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'Training_Attendance_December.xlsx')
    df_data = pd.read_excel(file_path, sheet_name='Report')

    # Rename the column names to standard format
    column_cleaner.standardise_column_names(df_data)

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_data, merge_dict)

    file_utilities.save_to_excel({'Test': data_with_brc_mapping}, 'TPD_with_BRC.xlsx')

    return data_with_brc_mapping

def run():
    """
    Function to call other internal functions and create the Common Pool reports
    """

    # Get the Commpon Pool data updated with BRC mapping
    data_with_brc_mapping = _get_data_with_brc_mapping()

    """# Get the elementary report
    #elem_report = get_tpd_training_elementary_report(data_with_brc_mapping.copy())

    # Get the secondary report
    #secnd_report = get_tpd_training_secondary_report(data_with_brc_mapping.copy())

     # Save the elementary report
    #file_utilities.save_to_excel({'TPD Training Elementary Report' : elem_report}, 'TPD Training Elementary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())   

    # Save the secondary report
    #file_utilities.save_to_excel({'TPD Training Secondary Report' : secnd_report}, 'TPD Training Secondary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())   """
    
    
    


if __name__ == "__main__":
    run()
