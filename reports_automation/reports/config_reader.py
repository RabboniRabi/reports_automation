"""
Module with functions to read the configurations given for each report in JSON format
"""

import json


def get_all_active_configs(config_file_name='report_configs.json'):
    """
    Function to fetch all the active report configurations given in the
    config JSON file.

    Parameters:
    -----------
    config_file_name: str
        The name of the file with all the configurations in JSON format. 
        Default is report_configs.json

    Returns:
    -------
    Returns array of configurations dictionaries where each item in the array is for each report
    """
    with open(config_file_name, 'r') as read_file:
        all_configs = json.load(read_file)["report_configs"]

    # Define a list of active configurations
    active_configs = []

    for config in all_configs:
        if config["generate_report"]:
            active_configs.append(config)

    # Close the file
    read_file.close()

    print('active_configs:', active_configs)

    return active_configs


def get_config(config_name, config_file_name='report_configs.json'):
    """
    Function to use the given config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
        The name of the config to search for
    config_file_name: str
        The name of the file with all the configurations in JSON format. 
        Default is report_configs.json
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    with open(config_file_name, 'r') as read_file:
        all_configs = json.load(read_file)["report_configs"]

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
