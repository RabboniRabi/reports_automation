import sys

import pandas as pd

sys.path.append('../')
import json

import readers.config_reader_v2 as config_reader
import readers.data_fetcher_v2 as data_fetcher


file_open = open("configs/10th_board_results.json", "r")
config = json.load(file_open)
source_config = config["source_config"]
source_data = source_config["sources"]
print(type(source_data[0]))
df_data = data_fetcher.get_data_from_config(source_data[0])
print(df_data)
file_open.close()



def main(raw_data, grouping_levels, agg_dict):
    """
    Function to group the student level data to school level data and performing aggregation on certain columns

    Args:
        raw_data:

    Returns:
    School-level dataframe
    """
    # Grouping the previous academic year student level data to school level
    prev_ac_yr_raw_data = raw_data.groupby(by=grouping_levels, as_index=False).agg(agg_dict)
    # Getting the Pass %
    prev_ac_yr_raw_data[cols.prev_pass_perc] = round(((prev_ac_yr_raw_data[cols.prev_pass]/prev_ac_yr_raw_data[cols.prev_tot_stu]) * 100), 2)

    # Deleting the unnecessary columns
    prev_ac_yr_raw_data.drop(columns=[cols.prev_pass, cols.prev_tot_stu], inplace=True)

    # Grouping the current academic year student level data to school level
    curr_ac_yr_raw_data = raw_data.groupby(by=grouping_levels, as_index=False).agg(agg_dict)
    # Getting the Pass %
    curr_ac_yr_raw_data[cols.curr_pass_perc] = round(((curr_ac_yr_raw_data[cols.curr_pass]/curr_ac_yr_raw_data[cols.curr_tot_stu])*100), 2)

    # Merging both the datasets
    raw_data = curr_ac_yr_raw_data.merge(prev_ac_yr_raw_data, how='left', on= grouping_levels)



