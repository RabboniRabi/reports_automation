"""
Sample code to demonstrate utilization of subtotaling functionality
"""

import os
import pandas as pd

import sys
sys.path.append('../')

from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook

#from reports_automation.utilities.subtotal_utilities import *
from utilities import subtotal_utilities
import utilities.subtotal_utilities as subtotal_utilities
import utilities.outlines_utilities as outlines_utilities





def main():

    curr_dir = os.path.dirname(os.path.realpath(__file__))

    sample_data_path = 'data/input'

    # Read the sample data for subtotals as a Pandas DataFrame object
    file_path = os.path.join(curr_dir, sample_data_path, 'subtotals.xlsx')
    df = pd.read_excel(file_path)

    # Define the levels and columns to subtotal
    level_subtotal_cols_dict = {1:'district_name', 2: 'edu_dist_name'}
    # Define the columns to aggregate and their respective aggregate function
    group_cols_agg_func_dict = {1:'sum', 2:'mean', 3:'sum'}
    # Define any additional text that need to be appended to the sub-totaled column values
    text_append_dict = {'district_name':'Total', 'edu_dist_name':'Sub-Total'}

    subtotal_outlines_dict = {}
    subtotal_outlines_dict['level_subtotal_cols_dict'] = level_subtotal_cols_dict
    subtotal_outlines_dict['agg_cols_func_dict'] = group_cols_agg_func_dict
    subtotal_outlines_dict['text_append_dict'] = text_append_dict

    # Create a ranking config - TODO
    ranking_config = {}



    # Compute sub-totals and insert into provided dataframe
    subtotals_result_dict = subtotal_utilities.compute_insert_subtotals(df, subtotal_outlines_dict, ranking_config)

    # Get the updated DataFrame object - with the subtotals inserted
    updated_df = subtotals_result_dict['updated_df']
    # Get only the subtotal rows
    df_subtotal_rows = subtotals_result_dict['subtotals']

    # Build outlines levels and ranges dictionary
    level_outline_ranges_dict = outlines_utilities.build_level_outline_ranges_dict(
        updated_df, df_subtotal_rows, level_subtotal_cols_dict, group_cols_agg_func_dict)

    # Convert the dataframe to an openpyxl object
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(updated_df, index=True, header=True):
        ws.append(r)

    # Apply the outlines function to the work sheet for the given levels and ranges
    outlines_utilities.apply_outlines(ws, level_outline_ranges_dict)

    output_data_path = 'data/output'

    write_path = os.path.join(curr_dir, output_data_path, 'subtotals_output.xlsx')

    wb.save(write_path)
    


if __name__ == "__main__":
    main()
