import sys

import pandas as pd

sys.path.append('../')

import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import utilities.utilities as utilities
import data_cleaning.column_cleaner as column_cleaner


# Fetch the configuration for creating the reports
    config = config_reader.get_config('10TH_BRD_MGMT_COMM_LVL_RPT', 'miscellaneous_configs')
    config = cols.update_nested_dictionaries(config)

# Get the source data configuration for the report code
    source_config_23 = report_configs['source_config_curr_yr']
    # Reading the Excel files as a dict
    df_data_set = data_fetcher.get_data_set_from_config(source_config_23, "miscellaneous_configs")

    source_config_22 = report_configs['sources_prev_yr']
    # Reading the Excel files as a dict
    df_data_set = data_fetcher.get_data_set_from_config(source_config_22, "miscellaneous_configs")

    # Fetch and prep the data
    df_prepped = tenth_board_community_acc.get_prepped_data_for_analysis(config)

    # Process the data before ranking
    process_config = config['process_args']
    df_processed = data_process_for_analysis(df_prepped, process_config)

