"""
Module with utility functions to format the reports for reviews,

The module will call the following utilities:
    - subtotal_utilities, to subtotal the data at different levels
    - outlines_utilities to apply Excel outlines on the data
    - format_utilities to apply different formatting styles on the data
"""

import os
import sys
sys.path.append('../')


import pandas as pd
import numpy as np
import utilities.file_utilities as file_utilities
import utilities.subtotal_utilities as subtotal_utilities
import utilities.outlines_utilities as outlines_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.format_utilities as format_utilities
import utilities.column_names_utilities as cols

import xlsxwriter

def prepare_report_for_review(df, report_config_dict, ranking_args_dict, sheet_name, file_name, dir_path):
    """
    Function to prepare the final report for viewing by:
        - computing subtotals
        - Applying Excel outlines
        - formatting the data
        - Saving the data
    Parameters:
    ----------
    df: Pandas DataFrame
        The report data that needs to be prepared
    report_config_dict: dict
        A dictionary of dictionaries to be used for computing subtotals and applying outlines
        Eg: secondary_report = {
            "generate_report": false,
            "ranking_args": {
                "agg_dict": {
                    "cols.ageing": "sum", 
                    "cols.total_cp_students": "sum"
                },
                "ranking_val_desc": "cols.perc_ageing",
                "num_col": "cols.ageing",
                "den_col": "cols.total_cp_students",
                "sort": true,
                "ascending": true
            },
            "subtotal_outlines_dict" : {
                "level_subtotal_cols_dict" : {"1" : "cols.deo_name_sec"},
                "agg_cols_func_dict" : {
                    "cols.fully_mapped": "sum",
                    "cols.part_mapped": "sum",
                    "cols.tot_schools": "sum",
                    "cols.deo_sec_rank": "mean"
                },
                "text_append_dict" : {"cols.deo_name_sec": "Total"}
            }
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

   
    # Get the subtotal and outlines specific configurations
    subtotal_outlines_dict = _update_subtotal_outlines_dict(report_config_dict['subtotal_outlines_dict'])
    level_subtotal_cols_dict = subtotal_outlines_dict['level_subtotal_cols_dict']
    agg_cols_func_dict = subtotal_outlines_dict['agg_cols_func_dict']
    text_append_dict = subtotal_outlines_dict['text_append_dict']


    # Compute sub-totals and insert into provided dataframe
    subtotals_result_dict = subtotal_utilities.compute_insert_subtotals(df, report_config_dict, ranking_args_dict)

    # Get the updated DataFrame object - with the subtotals inserted
    updated_df = subtotals_result_dict['updated_df']
    # Get only the subtotal rows
    df_subtotal_rows = subtotals_result_dict['subtotals']

    # Get and update the data frame with a grand total row at the bottom of the data set  
    grand_total_row = _get_grand_total_row(df, ranking_args_dict)
    print('grand_total_row: ', grand_total_row)
    updated_df.loc['Grand Total'] = grand_total_row

    # Remove rank for rows other than subtotal rows
    appended_col = list(text_append_dict.keys())[0]
    #if (appended_col == cols.deo_name_elm):
        #updated_df[~updated_df[appended_col].str.contains(text_append_dict[appended_col])][cols.deo_elem_rank] = ''
        #updated_df.loc[updated_df[~updated_df[appended_col].str.contains(text_append_dict[appended_col])] == True][cols.deo_elem_rank] = ''
        #updated_df[cols.deo_elem_rank] = np.where(~updated_df[appended_col].str.contains(text_append_dict[appended_col]), '', updated_df[cols.deo_elem_rank])

    # Build outlines levels and ranges dictionary
    level_outline_ranges_dict = outlines_utilities.build_level_outline_ranges_dict(
        updated_df, df_subtotal_rows, level_subtotal_cols_dict, agg_cols_func_dict)




    # Get the XlsxWriter object
    writer = file_utilities.get_xlsxwriter_obj({sheet_name: updated_df}, file_name, file_path=dir_path)

    # Get a XlsxWriter worksheet object
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name(sheet_name)
    
    """for r in dataframe_to_rows(updated_df, index=True, header=True):
        ws.append(r)"""

    # Apply the outlines function to the work sheet for the given levels and ranges
    outlines_utilities.apply_outlines(worksheet, level_outline_ranges_dict)

    #write_path = os.path.join(dir_path, file_name)

    # Save the data with subtotals and outlines
    writer.save()

    # Commenting out the section below as converting to xlsxWriter for formatting loses subtotaling and outlines.

    # Read the data again as XlsxWriter object
    # Needed to apply formatting on the data using XlsxWriter library functions
    #df_subtotaled = pd.read_excel(write_path)

    # Get an xlsx writer object of the data
    #writer = file_utilities.get_xlsxwriter_obj({sheet_name: df_subtotaled}, file_name, file_path=dir_path)
    
    # Get the formatting dictionary
    #format_dict = report_config_dict['format_dict']
    # If formatting dictionary has been provided
    #if (format_dict):
    """# Get the conditional format configuaration
    cond_format = format_dict['conditional_format']
    if cond_format:
        format = cond_format['format']
        # Apply this formatting to given list of columns
        for col_name in cond_format['columns']:
            # Get the index of the column
            col_index = df_subtotaled.columns.get_loc(col_name)
            no_of_rows = df_subtotaled.shape[0]
            # Apply the conditional formatting
            format_utilities.apply_cond_frmt(writer, sheet_name, col_index, format, no_of_rows)"""
    
    """# Get the cell format configuration
    format_cells = format_dict['format_cells']
    if format_cells:
        format = format_cells['format']
        # Apply cell formatting to given list of columns
        for col_name in format_cells['columns']:
            # Get the index of the column
            col_index = df_subtotaled.columns.get_loc(col_name)
            # Apply the cell formatting
            format_utilities.apply_cell_formatting(writer, sheet_name, col_index, format)"""
    




def _update_subtotal_outlines_dict(subtotal_outlines_dict:dict):
    """
    Internal function to update subtotal outline dict keys and values.
    
    When JSON configuration with variable keys and variable values are read
    as a dict, the variable resolution does not manually happen. 
    
    This utility function resolves the keys and values in the subtotal outlines dict
    
    Parameters:
    -----------
    subtotal_outlines_dict: dict
        The subtotal and outlines configuration dictionary fetched from JSON
    
    Returns:
    --------
    The updated subtotal outlines dictionary
    """

    # Update the subtotal level values
    level_subtotal_cols_dict = subtotal_outlines_dict['level_subtotal_cols_dict']
    for key in level_subtotal_cols_dict.keys():
        var_val = level_subtotal_cols_dict[key]
        updated_val = cols.get_value(var_val)
        level_subtotal_cols_dict[key] = updated_val

    # Update the aggregate columns function dictionary
    updated_agg_cols_func_dict = cols.update_dictionary_var_strs(subtotal_outlines_dict['agg_cols_func_dict'])
    subtotal_outlines_dict['agg_cols_func_dict'] = updated_agg_cols_func_dict

    # Update text append dict
    updated_text_append_dict = cols.update_dictionary_var_strs(subtotal_outlines_dict['text_append_dict'])
    subtotal_outlines_dict['text_append_dict'] = updated_text_append_dict

    return subtotal_outlines_dict
    

def _get_grand_total_row(df, ranking_args_dict):
    """
    Internal function to create a grand total row to insert at the bottom of the data set.

    Parameters:
    ----------
    df: Pandas DataFrame
        The data for which a grand total row has to be created
    ranking_args_dict: dict
        The ranking arguments dictionary that is reused to get the columns and aggregate functions
        to calculate the grand total

    Returns:
    -------
    The grand total row to insert
    """
    # Get the aggregate dictionary
    agg_dict = ranking_args_dict['agg_dict']
    no_of_columns = len(df.columns.to_list())
    
    # First set first cell as grand total and all cells in row to empty string. 
    grand_total_row = []
    for i in range(0, no_of_columns - 1):
        if i == 0:
            grand_total_row.append('Grand Total')
        # Set all other cells to blank
        grand_total_row.append('')
    
    # Then update specific cells present in agg_dict
    for key in agg_dict.keys():
        agg_func = agg_dict[key]
        if agg_func == 'sum':
            cell_total = df[key].sum()
        elif agg_func == 'mean':
            cell_total = df[key].mean()
        elif agg_func == 'count':
            cell_total = df[key].count()
        elif agg_func == 'median':
            cell_total = df[key].median()
        
        # Update the cell value for this column in grand total row
        grand_total_row[df.columns.get_loc(key)] = cell_total

    # Add the ranking value average to the row
    ranking_val_desc_col  = ranking_args_dict['ranking_val_desc']
    grand_total_row[df.columns.get_loc(ranking_val_desc_col)] = df[ranking_val_desc_col].mean()

    return grand_total_row
