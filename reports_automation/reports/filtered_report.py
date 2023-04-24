"""
Script to apply various sets of given filtering conditions to a dataset
and save the result as a generated report.
"""
import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities

import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import data_fetcher
import config_reader
import pandas as pd

def filter_data(df, filter_configs):
    """
    Function to filter the data using a given set of filtering conditions.
    Filtering will be sequentially applied in the order the conditions are given.

    Currently the filtering types are two: 'and_filters' and 'or_filters'
    In case of 'and_filters', the filters within that list are applied sequentially.
    In case of 'or_filters',  the filters on the data are applied separately and the final
    data is a merge result of all the separately filtered data. 

    Parameters:
    ----------
    df: Pandas DataFrame
        The data set to be filtered
    filter_configs: dict
        The dictionary of filters to be applied on the data
        Example: {
            "and_filters" : [
                {"col1" : ["val1", "val2"]},
                {"col2" : ["val3", "val4"]}
            ],
            "or_filters" : [
                {"col4" : ["val5", "val6"]},
                {"col5" : ["val7"]}
            ],            
        }
    """

    # Sequentially iterate through the filter configurations to apply the filters on the data
    for key, value in filter_configs.items():
        print('filter_config key: ', key)
        print('filter_config value: ', value)
        if key == 'and_filters':
            and_filters = value
            print('type of and filter: ', and_filters)
            for key,value in and_filters:
                # Apply the filter
                print('key is: ', key )
                print('value is: ', value)
                df = df[df[key] == value]

def main():
    """
    Main function that gets the data, the filter configurations and calls the relevant functions
    to filter the data and save it.
    """

    # Get the report configuration name/code given by the user
    filtered_report_config_name = sys.argv[1]
    config_category = None
    try: 
        config_category = sys.argv[2]
    except IndexError as error:
        print ('Category not given. All filtered_reports configs will be searched')

    if filtered_report_config_name is None:
        print ('No configuration code was provided. Kindly provide name/code of report as program argument.')

    report_config = config_reader.get_filtered_report_config(filtered_report_config_name, config_category)

    if report_config is None:
        # No report configuration was found.
        sys.exit('No report configuration found. Cannot generate the report!')

    source_config = report_config['source_config']
    df_data = data_fetcher.get_data_from_config(source_config)

    # Rename the column names to standard format
    column_cleaner.standardise_column_names(df_data)

    filter_configs = report_config['filter_configs']

    filtered_data = filter_data(df_data, filter_configs)

if __name__ == "__main__":
    main()