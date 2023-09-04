"""
Module with functions to create a report card/analysis of schools' performance
in 10th and 12th board exams with data compared to previous year and split
up district wise.
"""

import sys
sys.path.append('../')

import pandas as pd



import readers.config_reader as config_reader
import utilities.report_splitter_utilities as report_splitter
import readers.data_fetcher as data_fetcher
import utilities.ranking_utilities as ranking_utilities
import utilities.file_utilities as file_utilities
import utilities.format_utilities as format_utilities
import utilities.column_names_utilities as cols

import tenth_board_data_prep

def _get_overall_school_performance(marks):
    """
    Function to get overall school performance based on marks.
    Args:
        average_marks: column to grade

    Returns:
    School-wise performance data
    """
    if marks <= 35:
        return "Poor"
    elif(marks > 35) and (marks <= 50):
        return "Needs Improvement"
    elif (marks > 50) and (marks <= 70):
        return "Satisfactory"
    else:
        return "Good"

def data_process_for_analysis(df,process_config):
    """
    Function to process the data before the ranking.
    For Example:
        1. Finding the current academic year overall school performance
        2. Finding the difference in performance subject-wise
    Args:
        df:

    Returns:

    """
    # Getting the current and previous academic year overall school performance
    insert_cols_args_dict = process_config['school_performance']
    for col, insert_col_args in insert_cols_args_dict.items():
        # Get the school performance based on average marks
        # index = df.columns.get_loc(col) + insert_col_args['index_from_col']
        index = insert_col_args['index_from_col']
        df.insert(index, insert_col_args['insert_rank_col_name'], df[col].apply(_get_overall_school_performance))

    # Getting the columns to find the difference
    diff_args_dict = process_config['curr_yr_prev_yr_diff']
    for diff_col in diff_args_dict.keys():
        df[str(diff_col + "_difference")] = round(df[diff_col] - df[diff_args_dict[diff_col]], 2)
    return df


def create_district_wise_split_10th_board_reports():
    """
    Function to create split district wise reports
    for 10th board results
    """

    # Fetch the configuration for creating the reports
    config = config_reader.get_config('10th_board_dist_lvl_report_card', 'miscellaneous_configs')
    config = cols.update_nested_dictionaries(config)

    # Fetch and prep the data
    df_prepped = tenth_board_data_prep.get_prepped_data_for_analysis(config)

    # Process the data before ranking
    process_config = config['process_args']
    df_processed = data_process_for_analysis(df_prepped, process_config)


    # Rank the data at state level
    school_state_lvl_ranking_args = config['ranking_args_state']
    df_ranked_state = ranking_utilities.rank_cols_insert(df_processed, school_state_lvl_ranking_args)

    # Split data district wise and put them in a dictionary
    df_split_dist = report_splitter.split_report(df_ranked_state, cols.district_name)

    # For each item in the dictionary, call the ranking function to calculate rank in district
    school_dist_lvl_ranking_args = config['ranking_args_dist']
    for dist, df in df_split_dist.items():
        df_ranked_dist = ranking_utilities.rank_cols_insert(df, school_dist_lvl_ranking_args)
        # Updating the ranked dataframe to the corresponding district in the dictionary
        df_split_dist.update({dist: df_ranked_dist})

    format_save_reports(df_split_dist, config['format_configs'])



def format_save_reports(df_dict, format_configs):
    """
    Function to format the data in given dictionary of data sets and save.

    Parameters:
    -----------
    df_dict: dict
        Dictionary of data set, each of which needs to be formatted and saved
    format_configs: dict
        The format configurations to be applied on the data
    """

    # Get the number of state ranks in the data - to be used to append to 
    # state rank column headers
    no_of_state_ranks = 0
    for key in df_dict.keys():
        no_of_state_ranks += df_dict[key].shape[0]

    # Clean up data
    cols_to_drop = format_configs['cols_to_drop']
    cols_to_rename = format_configs['cols_to_rename']
    cols_order = format_configs['cols_order']
    for key in df_dict.keys():

        # Drop unncessary columns    
        df_dict[key].drop(columns=cols_to_drop, inplace=True)

        # Rename the columns
        df_dict[key].rename(columns=cols_to_rename, inplace=True)

        # Reorder the columns
        df_dict[key] = df_dict[key].reindex(columns=cols_order)

        # Sort the data by block and rank
        df_dict[key].sort_values(by=[cols.block_name, cols.rank_dist], inplace=True)

        no_of_dist_ranks = df_dict[key].shape[0]

        # Append the rank columns name with the number of ranks
        state_rank_cols = format_configs['cols_headers_to_be_appended_w_no_of_state_ranks']
        dist_rank_cols = format_configs['cols_headers_to_be_appended_w_no_of_dist_ranks']
        rank_cols_rename_dict = {}
        for rank_col in state_rank_cols:
            rank_cols_rename_dict[rank_col] = rank_col + ' (' + str(no_of_state_ranks) + ')'

        for rank_col in dist_rank_cols:
            rank_cols_rename_dict[rank_col] = rank_col + ' (' + str(no_of_dist_ranks) + ')'
        
        df_dict[key].rename(columns=rank_cols_rename_dict, inplace=True)

        

    # Convert the dictionary of data frames to dictionary of xlsxwriter objects for formatting
    dir_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('sslc_board_district_reports')
    xlsxwriters_dict = file_utilities.get_xlsxwriter_objs(df_dict, dir_path)
    
    # Get the formatting to be applied on all the datasets
    format_dicts_list = format_configs['format_dicts_list']

    # Format and Save the xlsxwriter objects
    for key in xlsxwriters_dict.keys():

        # Apply the formatting on the xlsxwriter object
        writer = xlsxwriters_dict[key]
        workbook = writer.book
        worksheet = workbook.get_worksheet_by_name(key)

        # Apply formatting specified in JSON
        format_utilities.apply_formatting(format_dicts_list, df_dict[key], worksheet, workbook, start_row=1)

        # Apply border to the data
        #format_utilities.apply_border(df_dict[key], worksheet, workbook)


        writer.save()
    
    


if __name__ == "__main__":
    create_district_wise_split_10th_board_reports()
