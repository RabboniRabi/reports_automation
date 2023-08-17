import sys

import pandas as pd

sys.path.append('../')
import json
import utilities.column_names_utilities as cols
import readers.config_reader_v2 as config_reader
import readers.data_fetcher_v2 as data_fetcher
import utilities.file_utilities as file_utilities
import data_cleaning.column_cleaner as column_cleaner

"""file_open = open("configs/10th_board_results.json", "r")
config = json.load(file_open)
source_config = config["source_config"]
source_data = source_config["sources"]
print(type(source_data[0]))
df_data = data_fetcher.get_data_from_config(source_data[0])
print(df_data)
file_open.close()"""

def get_prepped_data_for_analysis():
    """
    Function to prepare the 10th board results data for analysis

    Returns:
    --------

    """
    # Get the overall configuration for the report code
    report_config = config_reader.get_config("10TH_BRD_DIST_LVL_RPT_CARD", "miscellaneous_configs")
    source_config = report_config['source_config']
    df_data_set = data_fetcher.get_data_set_from_config(source_config, "miscellaneous_configs")

    # Getting previous academic year and current academic year as a separate dataframe
    prev_ac_yr_raw_data, curr_ac_yr_raw_data = df_data_set["prev_yr_data"], df_data_set["curr_yr_data"]

    # Rename the column names to standard format
    prev_ac_yr_raw_data = column_cleaner.standardise_column_names(prev_ac_yr_raw_data)
    curr_ac_yr_raw_data = column_cleaner.standardise_column_names(curr_ac_yr_raw_data)

    # Getting grouping levels and columns to aggregate information from the json
    grouping_levels = report_config['grouping_levels']
    agg_dict = report_config['agg_dict']
    prev_yr_agg_dict = agg_dict['prev_academic_year']
    curr_yr_agg_dict = agg_dict['curr_academic_year']

    # Grouping the previous academic year student level data to school level
    prev_ac_yr_raw_data = prev_ac_yr_raw_data.groupby(by=grouping_levels, as_index=False).agg(prev_yr_agg_dict)
    # Getting the Pass %
    prev_ac_yr_raw_data[cols.prev_pass_perc] = round(
        ((prev_ac_yr_raw_data[cols.prev_pass] / prev_ac_yr_raw_data[cols.prev_tot_stu]) * 100), 2)

    # Deleting the unnecessary columns
    prev_ac_yr_raw_data.drop(columns=[cols.prev_pass, cols.prev_tot_stu], inplace=True)

    # Grouping the current academic year student level data to school level
    curr_ac_yr_raw_data = curr_ac_yr_raw_data.groupby(by=grouping_levels, as_index=False).agg(curr_yr_agg_dict)
    # Getting the Pass %
    curr_ac_yr_raw_data[cols.curr_pass_perc] = round(
        ((curr_ac_yr_raw_data[cols.curr_pass] / curr_ac_yr_raw_data[cols.curr_tot_stu]) * 100), 2)

    # Merging both the datasets
    raw_data = curr_ac_yr_raw_data.merge(prev_ac_yr_raw_data, how='left', on=grouping_levels)
    raw_data.fillna({
        cols.prev_tot_marks: curr_ac_yr_raw_data[cols.curr_tot_marks],
        cols.prev_lang_marks: curr_ac_yr_raw_data[cols.curr_lang_marks],
        cols.prev_eng_marks: curr_ac_yr_raw_data[cols.curr_eng_marks],
        cols.prev_math_marks: curr_ac_yr_raw_data[cols.curr_math_marks],
        cols.prev_science_marks: curr_ac_yr_raw_data[cols.curr_science_marks],
        cols.prev_social_marks: curr_ac_yr_raw_data[cols.curr_social_marks],
        cols.prev_pass_perc: curr_ac_yr_raw_data[cols.curr_pass_perc]
    }, inplace=True)
    print(raw_data.columns)
    dir_path = file_utilities.get_gen_reports_dir_path()
    file_utilities.save_to_excel({"test": raw_data}, "10th_test_prev_yr_curr_yr.xlsx", dir_path=dir_path)

    return raw_data




if __name__ == "__main__":
    get_prepped_data_for_analysis()
