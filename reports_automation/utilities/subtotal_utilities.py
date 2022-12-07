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
import utilities.utilities as utilities

def compute_insert_subtotals(df, level_subtotal_cols_dict, group_cols_agg_func_dict, text_append_dict):
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
    group_cols_agg_func_dict: dict
        A grouping column - aggregate function dictionary. This dictionary contains the columns
        to group by as keys and their corresponding aggregating function as values
    text_append_dict: dict
        A dictionary of column names key and text values. The dictionary will be used
        to append text to values in each subtotaled column

    Returns:
    -------
    A dictionary with two values: 
    1) updated dataframe with inserted subtotals    
    2) dataframe with only subtotals rows
    Structure: {
        'updated_df': df,
        'subtotals': df_subtotal_rows
    }
    """

    # Get all the column names in the master data frame
    master_columns = df.columns.values

    # Initialize a data frame to hold the inserted subtotal rows
    df_subtotal_rows = pd.DataFrame(columns=df.columns) 

    # Get sorted levels
    levels = sorted(level_subtotal_cols_dict.keys())

    for level in levels:

        # Get the column to be subtotaled
        subtotal_col = level_subtotal_cols_dict[level]
        first_agg_col = True # Flag for merging grouped-aggregated values

        # For the column to be subtotaled, group and aggregate specified columns
        for agg_col in group_cols_agg_func_dict.keys():
            # Get the aggregate function for the column
            agg_func = group_cols_agg_func_dict[agg_col]
            # Group by the subtotal and aggregate the column by the aggregate function
            df_grouped = df.groupby([subtotal_col], as_index=False,sort=False)[agg_col].agg(agg_func)
            # Merge the aggregated columns into a single dataframe object
            if (first_agg_col):
                df_agg_cols_merged = df_grouped
                first_agg_col = False
            else:
                # Merge grouped-aggregate values for subtotal column
                df_agg_cols_merged = df_agg_cols_merged.merge(df_grouped[[subtotal_col, agg_col]])
                print('df_agg_cols_merged:', df_agg_cols_merged)
        
        # Merge all aggregagted values for column to be subtotaled into a single row
        # and insert into the original DataFrame object
        for i in range(0, df_agg_cols_merged.shape[0]):
            # Get the value of the cell in ith row and in column: subtotal_col
            
            subtotal_col_val = df_agg_cols_merged.loc[i, subtotal_col]
            
            # For non empty subtotal column values,
            if (subtotal_col_val != ''):

                # Get the indices in the master data frame matching this value in the same column
                matching_indices = df.index[df[subtotal_col] == subtotal_col_val].tolist()
                # Sort the list of matching indices (Will already be sorted. Just in case)
                matching_indices.sort()
                # Get the largest index value in the list
                last_matching_index = matching_indices[len(matching_indices) - 1]
                #print('largest_matching_index', last_matching_index)
                # Get the row with aggregated values to insert
                row_to_insert = df_agg_cols_merged.iloc[[i]]
                #print('row before building:', row_to_insert)
                
                # Make the row compatible for insertion with the original data frame
                row_to_insert = utilities.build_row(master_columns, row_to_insert, text_append_dict)
                #print('Row after building', row_to_insert)
                # Update a dataframe containing subtotal rows - to be used in outlines
                df_subtotal_rows.loc[df_subtotal_rows.shape[0]] = row_to_insert

                # Insert the aggregated row for this value below the last matching index
                print('Going to insert: ', row_to_insert, ' at index: ' , last_matching_index+1)
                df = utilities.insert_row(df, last_matching_index + 1, row_to_insert )

    # Return the updated DataFrame and subtotals DataFrame
    return {'updated_df': df, 'subtotals': df_subtotal_rows}




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


        


