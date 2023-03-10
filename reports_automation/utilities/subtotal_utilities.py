"""
Module with utility functions to perform subtotaling operations on datasets
"""

import os
import pandas as pd

import sys
sys.path.append('../')

from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook


import utilities.outlines_utilities as outlines_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols
import utilities.utilities as utilities

def compute_insert_subtotals(df, report_config_dict, ranking_args_dict):
    """
    Function to compute subtotals for a given set of columns. The order of computation
    of subtotals is based on the ascending order of levels. For each column to subtotal,
    the aggregation operations are applied to columns given to be aggregated.
    
    The function returns a Pandas DataFrame object of new subtotaled rows that have been
    inserted into the original DataFrame object
    
    Parameters:
    ----------
    df: Pandas DataFrame object
        The original DataFrame object on which subtotaling operations are to be performed
        and subtotal rows to be inserted
    level_subtotal_cols_dict: dict
        A level - subtotal column key value pair dictionary. The level determines the order
        of columns for which subtotaling aggregation operations are performed
    agg_cols_func_dict: dict
        A grouping column - aggregate function dictionary. This dictionary contains the columns
        to group by as keys and their corresponding aggregating function as values
    text_append_dict: dict
        A dictionary of column names key and text values. The dictionary will be used
        to append text to values in each subtotaled column

    Returns:
    -------
    A dictionary with three values: 
    1) updated dataframe with inserted subtotals    
    2) dataframe with only subtotals rows
    3) indices of inserted subtotal rows
    Structure: {
        'updated_df': df,
        'subtotals': df_subtotal_rows
        'subtotal_row_indices': subtotals_row_indices_list
    }
    """

    subtotal_outlines_dict = report_config_dict['subtotal_outlines_dict']

    level_subtotal_cols_dict = subtotal_outlines_dict['level_subtotal_cols_dict']
    agg_cols_func_dict = subtotal_outlines_dict['agg_cols_func_dict']
    text_append_dict = subtotal_outlines_dict['text_append_dict']

    # Get all the column names in the master data frame
    master_columns = df.columns.values

    # Initialize a data frame to hold the inserted subtotal rows - Useful for outlines and formatting
    df_subtotal_rows = pd.DataFrame(columns=df.columns) 

    # Initialize a list to hold the index locations of the inserted subtotal rows - Useful for formatting
    subtotals_row_indices_list = []

    # Get sorted levels
    levels = sorted(level_subtotal_cols_dict.keys())

    for level in levels:

        # Get the column to be subtotaled
        subtotal_col = level_subtotal_cols_dict[level]
        first_agg_col = True # Flag for merging grouped-aggregated values

        # Group by grouping levels and aggregate by given columns and aggregate function
        df_group_agg = df.groupby([subtotal_col], as_index=False,sort=False).agg(agg_cols_func_dict)

        # If ranking args dict is given
        if (ranking_args_dict):
            # Update the subtotal rows with ranking values
            df_group_agg = update_subtotaled_row_with_ranking_val(df_group_agg, ranking_args_dict)
        
        # Update the indices of the data frame before matching and inserting subtotal rows below
        df.reset_index(inplace=True, drop=True)
        
        # Merge all aggregagted values for column to be subtotaled into a single row
        # and insert into the original DataFrame object
        for i in range(0, df_group_agg.shape[0]):
            # Get the value of the cell in ith row and in column: subtotal_col
            
            subtotal_col_val = df_group_agg.loc[i, subtotal_col]
            
            # For non empty subtotal column values,
            if (subtotal_col_val != ''):

                # Get the indices in the master data frame matching this value in the same column
                matching_indices = df.index[df[subtotal_col] == subtotal_col_val].tolist()
                # Sort the list of matching indices (Will already be sorted. Just in case)
                matching_indices.sort()
                # Get the largest index value in the list
                last_matching_index = matching_indices[len(matching_indices) - 1]
                # Get the row with aggregated values to insert
                row_to_insert = df_group_agg.iloc[[i]]
                
                # Make the row compatible for insertion with the original data frame
                row_to_insert = utilities.build_row(master_columns, row_to_insert, text_append_dict)
                #print('Row after building', row_to_insert)
                # Update a dataframe containing subtotal rows - to be used in outlines
                df_subtotal_rows.loc[df_subtotal_rows.shape[0]] = row_to_insert

                # Insert the aggregated row for this value below the last matching index
                #print('Going to insert: ', row_to_insert, ' at index: ' , last_matching_index+1)
                df = utilities.insert_row(df, last_matching_index + 1, row_to_insert )

                # Update the list containing subtotal row indices - to be used in formatting
                subtotals_row_indices_list.append(last_matching_index + 1)

    # Return the updated DataFrame and subtotals DataFrame
    return {'updated_df': df, 'subtotals': df_subtotal_rows, 'subtotal_row_indices': subtotals_row_indices_list}


def update_subtotaled_row_with_ranking_val(df_subtotaled, ranking_args_dict):
    """
    Function to update the subtotaled row with ranking value.
    The ranking value cell for each subtotaled row is not summed, counted or taken a mean of
    as other columns as it will not represent a true value. The true value will depend on other columns.
    For example: percentage students attending classes will depend on present student/total student and not
    on the average percentages of sub-sections of the subtotal.

    Parameters:
    ----------
    df_subtotaled: Pandas DataFrame
        The subtotaled rows data
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
                'ranking_type' : 'percent_ranking',
                'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
                'ranking_val_desc' : '% moved to CP',
                'num_col' : 'class_1',
                'den_col' : 'Total',
                'sort' : True,
                'ascending' : False
                }
    Returns:
    --------
    Subtotal rows data updated with ranking values
    """
    ranking_args_dict['sort'] = False
    
    # Calculate ranking for the data with subtotal rows
    data_level_ranking = ranking_utilities.calc_ranking(df_subtotaled, None, ranking_args_dict)
    # Update the ranking value
    df_subtotaled[ranking_args_dict['ranking_val_desc']] = data_level_ranking[cols.ranking_value]

    return df_subtotaled


def subtotal_outline_and_save(df, level_subtotal_cols_dict, agg_cols_func_dict, sheet_name, file_name, dir_path, text_append_dict={}):
    """
    Helper function to compute subotals, apply outlines and save the data.

    Parameters:
    ----------
    df: Pandas DataFrame
        The data to work on
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

    # Compute sub-totals and insert into provided dataframe
    subtotals_result_dict = compute_insert_subtotals(
        df, level_subtotal_cols_dict, agg_cols_func_dict, text_append_dict)

    # Get the updated DataFrame object - with the subtotals inserted
    updated_df = subtotals_result_dict['updated_df']
    # Get only the subtotal rows
    df_subtotal_rows = subtotals_result_dict['subtotals']


    # Build outlines levels and ranges dictionary
    level_outline_ranges_dict = outlines_utilities.build_level_outline_ranges_dict(
        updated_df, df_subtotal_rows, level_subtotal_cols_dict, agg_cols_func_dict)

    # Convert the dataframe to an openpyxl object
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(updated_df, index=True, header=True):
        ws.append(r)

    # Apply the outlines function to the work sheet for the given levels and ranges
    outlines_utilities.apply_outlines(ws, level_outline_ranges_dict)

    write_path = os.path.join(dir_path, file_name)

    wb.save(write_path)


        


def format_subtotal_rows(worksheet, workbook, df, subtotal_row_indices):
    """
    Function to format the subtotal rows by styling it with border, background colour etc.

    Parameters:
    ----------
    worksheet: Worksheet
        An XlsxWriter worksheet object
    workbook: Workbook
        An XlsxWriter workbook object
    df: DataFrame
        The data containing subtotal rows
    subtotal_row_indices: list
        List of indices of subtotal rows in the dataframe
    """

    # Define the formatting to apply for all subtotal rows
    cell_format = workbook.add_format()
    # Set the subtotal rows to bold
    cell_format.set_bold() 
    # Set the subtotal row background to grey
    cell_format.set_bg_color('#949191')

    for row_index in subtotal_row_indices:
        #print('Applying subtotal formatting for row: ', row_index)
        worksheet.set_row(row_index + 1, None, cell_format)
    
