"""
Module with functions to read the configurations given for each report in JSON format
"""

import json

config_files = ['report_configs.json',
                'ceo_report_attendance_configs.json',
                'ceo_report_observations_configs.json',
                'ceo_report_operations_configs.json']

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
    all_active_configs = []

    for config_file_name in config_files:

        with open('configs/' + config_file_name, 'r') as read_file:
            all_configs = json.load(read_file)["report_configs"]

        # Define a list of active configurations
        active_configs = []

        for config in all_configs:
            if config["generate_report"]:
                active_configs.append(config)

        # Close the file
        read_file.close()

        # Update the full list of active configurations with the newly read configs
        all_active_configs.append(active_configs)

    return all_active_configs


def get_config(config_name:str, config_category:str=None, config_files:list=config_files):
    """
    Function to use the given config name and fetch the configuration to generate a report. 
    If no config is found, None is returned

    Parameters:
    ----------
    config_name: str
        The name/code of the config to search for
    config_category: str
        The category of configuration. This will be used to search for the 
        configuration in the JSON file matching the config category. 
        Default is None. All available configuration files will be searched.
    config_files: list
        The file names of all the configurations in JSON format. 
        Default is the list declared in the script
    
    Returns:
    --------
    A dictionary of config values for the report. None Object if no config is found.
    """
    if config_category is not None:

        # Assume that the configuration filename matches the configuration category
        config_file_name = config_category + '.json'
        with open('configs/' + config_file_name, 'r') as read_file:
            all_configs = json.load(read_file)["report_configs"]

        for config in all_configs:
            if config["report_name"] == config_name or config["report_code"] == config_name:
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
                
                all_configs = json.load(read_file)["report_configs"]

                for config in all_configs:
                    if config["report_name"] == config_name or config["report_code"] == config_name:
                        # Close the file
                        read_file.close()
                        return config

                # Close the file
                read_file.close()
        return None

    

if __name__ == "__main__":
    #print(type(get_config('PETS')))
    get_all_active_configs()