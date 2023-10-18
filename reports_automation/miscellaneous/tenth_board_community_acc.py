import sys

sys.path.append('../')

import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import utilities.file_utilities as file_utilities
import tenth_board_data_prep

# Fetch the configuration for creating the reports
config = config_reader.get_config('10TH_BRD_MGMT_COMM_LVL_RPT', 'miscellaneous_configs')
config = cols.update_nested_dictionaries(config)

df_dict = config['source_config_curr_yr']

# Fetch the grouping_level configuration for creating the reports
grouping_level = config['grouping_levels']

# Fetch the agg_dict configuration for creating the reports
agg_dict = config['agg_dict']

col_name_to_concat = config['']

# Fetch the filter_dict configuration for creating the reports
filter_dict = config['filter_dict']

# Read the current year board results data as a Pandas DataFrame dictionary
source_config_curr_yr = config['source_config_curr_yr']
source_config_curr_yr = data_fetcher.get_data_set_from_config(source_config_curr_yr, "miscellaneous_configs")

# Reading the Excel files as a dict
sources_prev_yr = config['sources_prev_yr']
sources_prev_yr = data_fetcher.get_data_set_from_config(sources_prev_yr, "miscellaneous_configs")

# Fetch and grouping level data
df_10th = tenth_board_data_prep.get_grouping_level_data(grouping_levels=grouping_level, agg_dict=agg_dict,
                                                        filter_dict=filter_dict)

# Save the report
file_utilities.save_to_excel({'10th_comm_wise_report': df_10th}, '10th_comm_wise_report.xlsx', index=True)


def get_metric_grouped_data(source_config, df_dict, grouping_levels, agg_dict, col_name_to_concat, filter_dict):
    """

    Returns:

    """

    # Fetch the configuration for creating the reports
    config = config_reader.get_config('10TH_BRD_MGMT_COMM_LVL_RPT', 'miscellaneous_configs')
    config = cols.update_nested_dictionaries(config)

    # Read the current year board results data as a Pandas DataFrame dictionary
    source_config_curr_yr = config['source_config_curr_yr']
    sources_curr_yr = data_fetcher.get_data_set_from_config(source_config_curr_yr, "miscellaneous_configs")

    # Reading the Excel files as a dict
    sources_prev_yr = config['sources_prev_yr']
    sources_prev_yr = data_fetcher.get_data_set_from_config(sources_prev_yr, "miscellaneous_configs")

    # Fetch the grouping_level configuration for creating the reports
    grouping_level = config['grouping_levels']
    df_dict = config['source_config_curr_yr']
    agg_dict = config['agg_dict']
    filter_dict = config['filter_dict']
    col_name_to_concat = config['']

    for comm in grouping_level:
        # Fetch and grouping level data
        df_10th[comm] = tenth_board_data_prep.get_grouping_level_data(df_dict=df_dict, grouping_levels=grouping_level, agg_dict=agg_dict,
                                                                filter_dict=filter_dict)



