"""
This module contains functions to fetch raw data
"""

import os
import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities

import pandas as pd

import config_reader



def get_data_from_config(source_config_dict, save_source=False):
    """
    This function fetches the given source data configuration.

    Depending on the configuration, the function fetches the data from the
    database or from a source excel file, with first preference given for database fetch.

    An option to save the source data fetched is provided. It is disabled by default.

    Parameters
    ----------
    source_config_dict: dict
        This dict will be the source_config nested json that has the query/excel file information which needs to be
        pulled.

    save_source: bool
        Flag to indicate if a copy of the source data pulled from the database needs to be saved.
        Default is False. If the raw data needs to be saved, the flag should be true 
        and the data will be saved to the current month's source data folder.

    Returns
    -------
        A dataframe with the raw data based on the source_config
    """

    df_data = None

    if source_config_dict is None:
        # No source configuration was found
        sys.exit('The provided source configuration is empty')


    # If query file name is given in source configuration
    if "query_file_name" in source_config_dict:

        query_file_name = source_config_dict.get('query_file_name')


        try:
            # Read the database connection credentials
            credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
            # Fetch the data from the query
            df_data = dbutilities.fetch_data_as_df(credentials_dict, query_file_name)
            # If save source flag has been enabled, save to the source data folder
            if save_source:
                save_file_name = query_file_name.split(".")[0] +'_'+utilities.get_today_date() + '.xlsx'
                file_utilities.save_to_excel({query_file_name: df_data}, save_file_name,
                                dir_path=file_utilities.get_curr_month_source_data_dir_path())
            return df_data
        except Exception as err:
            print(f'Error: ', err)
    elif "source_file_name" in source_config_dict:

        # Fetch from Excel source data location
        source_file_name = source_config_dict['source_file_name']
        print('Reading data from ' + source_file_name + ' file...')
        try:
            sheet_name = source_config_dict['source_sheet_name']
            skip_rows = source_config_dict['skip_rows']
        except KeyError as err:
            err_msg = 'Missing configurations in: ' + str(source_config_dict)
            sys.exit(err_msg)
        # The file is assumed to be in the current month's source data folder
        file_path = os.path.join(file_utilities.get_curr_month_source_data_dir_path(), source_file_name)
        
        df_data = pd.read_excel(file_path, sheet_name, skiprows=skip_rows)
        print('Data read successful.')
    else:
        # No source configuration was found
        sys.exit('No source configuration found')

    return df_data


def get_data(report_code, save_source=False):
    """
    This function fetches the data by getting and using the appropriate
    source data configuration from the report_configs.json file
    for a given report code.

    Depending on the configuration, the function fetches the data from the
    database or from a source excel file.

    An option to save the source data fetch is provided. It is disabled by default.

    Parameters
    ----------
    report_code: str
        The name/code of the report/metric to fetch the data for
    save_source: bool
        Flag indicating if a copy of data fetched from database needs to be saved.
        To be used within the application. Default is False.

    Returns
    -------
    Raw data as a Pandas DataFrame object
    """
    # Get the overall configuration for the report
    config = config_reader.get_config(report_code)

    # Get the source data configuration for the report
    source_config = config.get('source_config')

    # Get the data
    df_data = get_data_from_config(source_config, save_source)

    return df_data


# For testing
if __name__ == "__main__":
    # Declare a source config
    """source_config = {
            "source_file_name" : "Pet-to-school-Mapping-Rpt.xlsx",
            "source_sheet_name" : "Report",
            "skip_rows" : 4
        }"""
    #df_raw_data = get_data_from_config(source_config)
    df_raw_data = get_data('PET',save_source=True)
    print('columns of df_raw_data fetched: ', df_raw_data.columns.to_list())
