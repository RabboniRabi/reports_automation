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
import readers.data_fetcher_v2 as data_fetcher
import utilities.file_utilities as file_utilities

import tenth_board_data_prep


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

    # Rank the data at state level
    school_state_lvl_ranking_args = config['ranking_args_state']
    df_ranked_state = ranking_utilities.rank_cols_insert(df_prepped, school_state_lvl_ranking_args)

    # Split data district wise and put them in a dictionary

    # For each item in the dictionary, call the ranking function to calculate rank in district

    # Save each district data as a separate file in a sub-folder






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
