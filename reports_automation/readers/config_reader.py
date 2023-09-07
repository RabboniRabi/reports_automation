"""
Module with functions to read the JSON configurations to generate reports
"""
import os
import sys
sys.path.append('../')

import json
from collections import OrderedDict

import utilities.file_utilities as file_utilities

from readers.config_types import ConfigTypes as config_types

__curr_location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_all_active_ceo_review_configs():
    """
    Function to fetch all the active ceo review report generation JSON configurations
    as a list of dictionaries

    Returns:
    -------
    Returns array of configurations dictionaries where each item in the list 
    is the configuration for each report
    """
    # Define a list of active configurations
    active_configs = []

    # Load the JSON file with the locations of all the config files
    file_path = os.path.join(__curr_location__, 'config_files_locations.json')

    with open(file_path, 'r') as read_file:
            config_files_locations = json.load(read_file)        

    # Get the ceo review reports specific config files location information
    ceo_configs_loc_info = config_files_locations['ceo_review_configs']

    # For each file with the configurations
    for file_name in ceo_configs_loc_info['files']:
        # Build the path to the file given to contain the config
        config_file_path = file_utilities.build_file_path(file_name, ceo_configs_loc_info['dir_levels'])

        # Read the file
        with open(config_file_path, 'r') as read_file:
            all_configs = json.load(read_file)['report_configs']

        for config in all_configs:
            if config["generate_report"]:
                active_configs.append(config)

        # Close the file
        read_file.close()

    return active_configs


def get_config(config_code:str, config_category:str, config_file_name:str=None):
    """
    Function to use the given config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_code: str
        The name/code of the config to search for
    config_category: str
        The category of configuration. This will be used to search for the 
        configuration in the directory containing configuration files for this category. 
        Default is None. All available configuration files will be searched.
    config_file_name: str
        The name of the file where the configuration is. Default is None. If None, all files in
        the config_category directory are searched for the config
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """

    # Load the JSON file with the locations of all the config files
    file_path = os.path.join(__curr_location__, 'config_files_locations.json')

    with open(file_path, 'r') as read_file:
            config_files_locations = json.load(read_file)        

    # Get the config category specific config files location information
    config_cat_specific_loc_info = config_files_locations[config_category]

    if config_file_name is not None:
        # Build the path to the file given to contain the config
        config_file_path = file_utilities.build_file_path(config_file_name, config_cat_specific_loc_info['dir_levels'])

        # Read the file
        with open(config_file_path, 'r') as read_file:
            all_configs = json.load(read_file)

        for config in all_configs:
            if config["report_name"] == config_code or config["report_code"] == config_code:
                # Close the file
                read_file.close()
                return config
            else:
                print('Configuration not found in: ', config_file_path)
                # Close the file
                read_file.close()
                return None

    
    else:
        # Build the path to the folder containing the category specific configuration files
        config_files_dir = file_utilities.build_dir_path(config_cat_specific_loc_info['dir_levels'])

        # Get all the config files for the category
        config_files = config_cat_specific_loc_info['files']

        # Read each one and check if the code is there
        for config_file in config_files:
            with open(os.path.join(config_files_dir, config_file), 'r') as read_file:
                
                all_configs = json.load(read_file)["report_configs"]

                for config in all_configs:
                    if config["report_name"] == config_code or config["report_code"] == config_code:
                        # Close the file
                        read_file.close()
                        return config

                # Close the file
                read_file.close()
        return None


def get_adhoc_config(config_code:str, config_file_name:str=None):
    """
    Function to use the given ad hoc config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_code: str
        The name/code of the ad hoc config to search for
    config_file_name: str
        The name of the file where the configuration is. Default is None. If None, all files in
        the config_category directory are searched for the config
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    return get_config(config_code, config_types.AD_HOC.value, config_file_name)



def get_ceo_rpt_config(config_code:str, config_file_name:str=None):
    """
    Function to use the given ceo report config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_code: str
        The name/code of the ceo report config to search for
    config_file_name: str
        The name of the file where the configuration is. Default is None. If None, all files in
        the config_category directory are searched for the config
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    return get_config(config_code, config_types.CEO_REVIEW.value, config_file_name)

def get_misc_rpt_config(config_code:str, config_file_name:str=None):
    """
    Function to use the given miscellane report config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_code: str
        The name/code of the ceo report config to search for
    config_file_name: str
        The name of the file where the configuration is. Default is None. If None, all files in
        the config_category directory are searched for the config
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    return get_config(config_code, config_types.MISCELLANEOUS.value, config_file_name)

