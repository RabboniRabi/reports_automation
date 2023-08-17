"""
Module with functions to read the configurations given for each report in JSON format
"""
import os
import sys
sys.path.append('../')

import json
from collections import OrderedDict

import utilities.file_utilities as file_utilities

__curr_location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

ceo_review_config_files = ['ceo_review/attendance_configs.json',
                'ceo_review/board_results_configs.json',
                'ceo_review/class_configs.json',
                'ceo_review/cwsn_configs.json',
                'ceo_review/cwsn_transition_configs.json',
                'ceo_review/enrolment_configs.json',
                'ceo_review/health_configs.json',
                'ceo_review/library_configs.json',
                'ceo_review/observations_configs.json',
                'ceo_review/oosc_configs.json',
                'ceo_review/schemes.json',
                'ceo_review/student_transition_configs.json',
                'ceo_review/sports_configs.json',
                'ceo_review/training_attendance.json',
                'ceo_review/tc_issued_configs.json',
                'ceo_review/g2c_configs.json']

ad_hoc_config_files = ['ad_hoc/attendance_configs.json',
                        'ad_hoc/cg_configs.json',
                        'ad_hoc/updation_status_configs.json']

misc_config_files = ['../miscellaneous/10th_board_data_prep.json']

filtered_report_config_files = ['filtered_reports/teachers.json']

config_files = ceo_review_config_files + ad_hoc_config_files + filtered_report_config_files

def get_all_active_configs(config_files:list=config_files):
    """
    Function to fetch all the active report configurations given in the
    config JSON files.

    Parameters:
    -----------
    config_files: list
        The file names of all the configurations in JSON format. 
        Default is the list declared in the script

    Returns:
    -------
    Returns array of configurations dictionaries where each item in the dictionary is for each report
    """
    # Define a list of active configurations
    active_configs = []

    for config_file_name in config_files:

        with open('configs/' + config_file_name, 'r') as read_file:
            all_configs = json.load(read_file)["report_configs"]

        for config in all_configs:
            if config["generate_report"]:
                active_configs.append(config)

        # Close the file
        read_file.close()

    return active_configs


def get_config(config_name:str, config_category:str, config_file_name:str=None):
    """
    Function to use the given config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
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
        config_file_path = file_utilities.build_file_path(config_file_name+'.json', config_cat_specific_loc_info['dir_levels'])

        # Read the file
        with open(config_file_path, 'r') as read_file:
            all_configs = json.load(read_file)['report_configs']

        for config in all_configs:
            if (config["report_name"] == config_name) or (config["report_code"] == config_name):
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
                
                all_configs = json.load(read_file)['report_configs']

                for config in all_configs:
                    if config["report_name"] == config_name or config["report_code"] == config_name:
                        # Close the file
                        read_file.close()
                        return config

                # Close the file
                read_file.close()
        return None


def get_adhoc_config(config_name:str, config_category:str=None, config_files:list=ad_hoc_config_files):
    """
    Function to use the given ad hoc config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
        The name/code of the ad hoc config to search for
    config_category: str
        The category of configuration. This will be used to search for the 
        configuration in the JSON file matching the config category. 
        Default is None. All available configuration files will be searched.
    config_files: list
        The file names of all the configurations in JSON format. 
        Default is the list of ad hoc config files declared in the script
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    return get_config(config_name, config_category, config_files)



def get_ceo_rpt_config(config_name:str, config_category:str=None, config_files:list=ceo_review_config_files):
    """
    Function to use the given ceo report config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
        The name/code of the ceo report config to search for
    config_category: str
        The category of configuration. This will be used to search for the 
        configuration in the JSON file matching the config category. 
        Default is None. All available configuration files will be searched.
    config_files: list
        The file names of all the configurations in JSON format. 
        Default is the list of ad hoc config files declared in the script
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    return get_config(config_name, config_category, config_files)       

def get_misc_rpt_config(config_name:str, config_category:str=None, config_files:list=misc_config_files):
    """
    Function to use the given miscellane report config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
        The name/code of the ceo report config to search for
    config_category: str
        The category of configuration. This will be used to search for the 
        configuration in the JSON file matching the config category. 
        Default is None. All available configuration files will be searched.
    config_files: list
        The file names of all the configurations in JSON format. 
        Default is the list of ad hoc config files declared in the script
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    return get_config(config_name, config_category, config_files)      

def get_filtered_report_config(config_name:str, config_category:str=None, config_files:list=filtered_report_config_files):
    """
    Function to use the given filtered config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
        The name/code of the ad hoc config to search for
    config_category: str
        The category of configuration. This will be used to search for the 
        configuration in the JSON file matching the config category. 
        Default is None. All available configuration files will be searched.
    config_files: list
        The file names of all the configurations in JSON format. 
        Default is the list of ad hoc config files declared in the script
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    if config_category is not None:

        # Assume that the configuration filename matches the configuration category
        config_file_name = config_category + '.json'
        with open('configs/filtered_reports' + config_file_name, 'r') as read_file:
            # Using a ordered dict to load the JSON as the order of configurations matter
            all_configs = json.load(read_file, object_pairs_hook=OrderedDict)["report_configs"]

        for config in all_configs:
            if config["report_name"] == config_name:
                # Close the file
                read_file.close()
                return config

        # Close the file
        read_file.close()
        return None
    else:
        # Iterate through all the configuration files to search for the given configuration code/name
        for config_file_name in config_files:
            with open('configs/' + config_file_name, 'r') as read_file:
                
                all_configs = json.load(read_file, object_pairs_hook=OrderedDict)["report_configs"]

                for config in all_configs:
                    if config["report_name"] == config_name:
                        # Close the file
                        read_file.close()
                        return config

                # Close the file
                read_file.close()
        return None



if __name__ == "__main__":
    #print(type(get_config('PETS')))
    get_all_active_configs()
