"""
This module contains functions to fetch raw data
"""

import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities


import pandas as pd



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
            This parameter would by default not save the raw data pulled by the function. If the raw data needs to be
            saved, the flag should be true and the data will be to the mentioned folder.

    Returns
    -------
        A dataframe with the raw data based on the source_config
    """

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # If query file name is given in source configuration
    if "query_file_name" in source_config_dict:

        query_file_name = source_config_dict.get('query_file_name')
        try:
            # Fetch the data from the query
            df_data = dbutilities.fetch_data_as_df(credentials_dict, query_file_name)
            # If save source flag has been enabled, save to the source data folder
            if save_source:
                file_utilities.save_to_excel({query_file_name: df_data}, query_file_name + '.xlsx')
        except Exception as err:
            print(f'Error: ', err)
    elif "source_file_name" in source_config_dict:

        # Fetch from Excel source data location
        source_file_name = source_config_dict.get('source_file_name')
        df_data = pd.read_excel(source_file_name,'r')
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
    report_code
    save_source

    Returns
    -------

    """
