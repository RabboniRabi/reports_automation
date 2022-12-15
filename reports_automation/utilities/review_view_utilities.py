"""
Module with utility functions to format the reports for reviews,

The module will call the following utilities:
    - subtotal_utilities, to subtotal the data at different levels
    - outlines_utilities to apply Excel outlines on the data
    - format_utilities to apply different formatting styles on the data
"""

import sys
sys.path.append('../')

import utilities.subtotal_utilities as subtotal_utilities
import utilities.outlines_utilities as outlines_utilities

def prepare_report_for_review(df, subtotal_outlines_dict, format_dict, sheet_name, file_name, dir_path):
    """
    Function to prepare the final report for viewing by:
        - computing subtotals
        - Applying Excel outlines
        - formatting the data
    Parameters:
    ----------
    df: Pandas DataFrame
        The report data that needs to be prepared
    subtotal_outlines_dict: dict
        A dictionary of dictionaries to be used for computing subtotals and applying outlines
        Eg: subtotal_outlines_dict = {
            'level_subtotal_cols_dict' : {1:'district_name', 2: 'edu_dist_name'}
            'agg_cols_func_dict' : {'screened':'sum', 'schools':'count', 'rank':'mean'}
            'text_append_dict' : {'district_name':'Total', 'block_name':'Sub-Total'}

        }
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : True, 
        'ascending' : False
        }
    level_subtotal_cols_dict: dict
        A level - subtotal column key value pair dictionary. The level determines the order
        of columns for which subtotaling aggregation operations are performed
    agg_cols_func_dict: dict
        A grouping column - aggregate function dictionary. This dictionary contains the columns
        to group by as keys and their corresponding aggregating function as values
    sheet_name: str
        The name of the sheet to save the data in.
    file_name: str
        The name of the file to save the data sheet in.
    dir_path: str
        The directory in which to save the file in.
    text_append_dict: dict
        A dictionary of column names key and text values. The dictionary will be used
        to append text to values in each subtotaled column. Default is {}
    """