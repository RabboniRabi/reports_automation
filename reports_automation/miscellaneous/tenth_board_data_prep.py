import sys

import pandas as pd

sys.path.append('../')
import json
import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import data_cleaning.column_cleaner as column_cleaner


def get_prepped_data_for_analysis(report_config):
    """
    Function to prepare the 10th board results data for analysis

    Parameters:
    ----------
    report_config: dict
        The configuration containing variable values that will be used to prepare the data

    Returns:
    --------
    Data prepared as a data frame object

    """
    # Get the source data configuration for the report code
    source_config = report_config['source_config']
    # Reading the Excel files as a dict
    df_data_set = data_fetcher.get_data_set_from_config(source_config, "miscellaneous_configs")

    # Getting previous academic year and current academic year as a separate dataframe
    prev_ac_yr_raw_data, curr_ac_yr_raw_data = df_data_set["prev_yr_data"], df_data_set["curr_yr_data"]

    # Rename the column names to standard format
    prev_ac_yr_raw_data = column_cleaner.standardise_column_names(prev_ac_yr_raw_data)
    curr_ac_yr_raw_data = column_cleaner.standardise_column_names(curr_ac_yr_raw_data)

    # Getting grouping levels and columns to aggregate information from the json
    grouping_levels = report_config['grouping_levels']
    agg_dict = report_config['agg_dict']


    # Grouping the previous academic year student level data to school level
    #prev_ac_yr_raw_data = prev_ac_yr_raw_data.groupby(by=grouping_levels, as_index=False).agg(prev_yr_agg_dict)
    prev_ac_yr_schl_lvl = utilities.group_agg_rename(prev_ac_yr_raw_data, grouping_levels, agg_dict, 'prv_yr')
    
    # Add the Pass % at school level
    prev_ac_yr_schl_lvl[cols.prev_pass_perc] = round(
        ((prev_ac_yr_schl_lvl[cols.prev_pass] / prev_ac_yr_schl_lvl[cols.prev_tot_stu]) * 100), 2)

    # Add the average median marks at school level
    prev_ac_yr_schl_lvl[cols.prev_avg_marks] = round((prev_ac_yr_schl_lvl[cols.prev_tot_marks] / 5), 2)

    # Deleting the unnecessary columns
    prev_ac_yr_schl_lvl.drop(columns=[cols.prev_pass, cols.prev_tot_stu, cols.prev_tot_marks], inplace=True)

    # Grouping the current academic year student level data to school level
    #curr_ac_yr_raw_data = curr_ac_yr_raw_data.groupby(by=grouping_levels, as_index=False).agg(curr_yr_agg_dict)
    curr_ac_yr_schl_lvl = utilities.group_agg_rename(curr_ac_yr_raw_data, grouping_levels, agg_dict,'curr_yr')

    # Getting the Pass %
    curr_ac_yr_schl_lvl[cols.curr_pass_perc] = round(
        ((curr_ac_yr_schl_lvl[cols.curr_pass] / curr_ac_yr_schl_lvl[cols.curr_tot_stu]) * 100), 2)
    
    # Add the average median marks at school level
    curr_ac_yr_schl_lvl[cols.curr_avg_marks] = round((curr_ac_yr_schl_lvl[cols.curr_tot_marks] / 5), 2)

    # Deleting the unnecessary columns
    curr_ac_yr_schl_lvl.drop(columns=[cols.curr_tot_marks], inplace=True)

    # Merging both the datasets
    merged_schl_lvl_data = pd.merge(curr_ac_yr_schl_lvl, prev_ac_yr_schl_lvl, how='left', on=grouping_levels)

    # Filling the null values with the current academic year values
    merged_schl_lvl_data.fillna({
        cols.prev_avg_marks: curr_ac_yr_schl_lvl[cols.curr_avg_marks],
        cols.prev_lang_marks: curr_ac_yr_schl_lvl[cols.curr_lang_marks],
        cols.prev_eng_marks: curr_ac_yr_schl_lvl[cols.curr_eng_marks],
        cols.prev_math_marks: curr_ac_yr_schl_lvl[cols.curr_math_marks],
        cols.prev_science_marks: curr_ac_yr_schl_lvl[cols.curr_science_marks],
        cols.prev_social_marks: curr_ac_yr_schl_lvl[cols.curr_social_marks],
        cols.prev_pass_perc: curr_ac_yr_schl_lvl[cols.curr_pass_perc]
    }, inplace=True)


    return merged_schl_lvl_data




if __name__ == "__main__":
    get_prepped_data_for_analysis()
