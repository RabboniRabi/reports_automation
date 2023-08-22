"""
Module with functions to create a report card/analysis of schools' performance
in 10th and 12th board exams with data compared to previous year and split
up district wise.
"""

import sys
sys.path.append('../')

import pandas as pd

import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols
import readers.config_reader_v2 as config_reader
import utilities.report_splitter_utilities as report_splitter
import readers.data_fetcher_v2 as data_fetcher
import utilities.file_utilities as file_utilities

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
        df[str(diff_col + "_difference")] = df[diff_col] - df[diff_args_dict[diff_col]]
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

    # Save each district data as a separate file in a sub-folder
    report_splitter.save_split_report(df_split_dist, "sslc_board_district_reports")






# Testing formatting in XLSX writer
"""
writer = file_utilities.get_xlsxwriter_obj(
	{'10th_SCHL_LVL': df_merged}, 
	'10th_marks_schl_lvl.xlsx',
	file_path='/home/rabboni/Documents/EMIS/Data Reporting/reports/extracted/Aug_23/')


writer.sheets['10th_SCHL_LVL'].conditional_format('F2:F5613', {'type': 'icon_set',
                                                         'icon_style': '3_arrows',
                                                         'icons': [
                  {'criteria': '>', 'type': 'number', 'value': '0'},
                  {'criteria': '==', 'type': 'number', 'value': '0'}
                                                         ]}
                                            )



print('saving sheeting after formatting')
writer.save()
"""



if __name__ == "__main__":
    create_district_wise_split_10th_board_reports()
