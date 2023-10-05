import sys

import pandas as pd

sys.path.append('../')

import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import utilities.utilities as utilities
import data_cleaning.column_cleaner as column_cleaner

def get_grouping_level_data(df_dict, grouping_levels, agg_dict, col_name_to_concat):
    """
    Function to group student level data for different management types and build
    a consolidated dataframe. Additionally, data is grouped with the given grouping level
    minus the management type to get aggregated data at 'all management' level.

    For example, grouping levels can be ['District', 'Block', 'management'].
    The function will group and return data as:
        district A | Block i | Govt | aggregated data
        district A | Block i | Aided | aggregated data
        .
        .
        district A | Block i | All Management | aggregated data
        district A | Block ii | Govt | aggregated data
        .
        .

    Parameters:
    ----------
    df_dict: dict
        Management type - student data key-value pairs
    agg_dict: dict
        For Example:
            "agg_dict": {
                "cols.tot_stu": "count",
                "cols.stu_pass": "sum",
                "cols.lang_marks": "median",
                "cols.eng_marks": "median"
            }
    grouping_levels: list
        For Example to group at a block level: ["cols.district_name", "cols.block_name", "cols.management"]
    col_name_to_concat: str
        To concatenate new string value to the aggregate columns
        For Example: 'curr_yr'
    filter_dict: dict
        Data cleaning - excluding invalid values from the dataframe

    Returns:
    -------
    Grouped consolidated data frame
    """

    # Creating an empty dataframe
    df_master = pd.DataFrame()


    # For each school management type dataframe grouping at a given grouping level
    for management_type, df in df_dict.items():

        # Data cleaning - excluding invalid values from the dataframe
        #df = utilities.filter_dataframe(df, filter_dict, include=False)

        # Concatenating each management type dataframe into a single master dataframe
        # df_master is to be used afterwards for grouping to 'all management' level
        df_master = pd.concat([df_master, df])
        # Grouping each management type df at a given grouping level
        df = utilities.group_agg_rename(df, grouping_levels, agg_dict, col_name_to_concat)
        # Replace student level data with grouped data in dictionary
        df_dict.update({management_type: df})

    # Consolidate grouped data for each management type into a single dataframe
    merged_df = pd.concat(df_dict.values())

    # Rename values in previously built df_master for the column management type to 'all management'
    # To help in grouping to all management level
    df_master[cols.management] = cols.all_management

    # Group and aggregate on this data
    df_master = utilities.group_agg_rename(df_master, grouping_levels, agg_dict, col_name_to_concat)

    # Concatenate 'all management' grouped data and management type consolidated grouped data
    df_master = pd.concat([df_master, merged_df])

    return df_master
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

