"""
Module with utility functions to format the reports for reviews

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
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.subtotal_utilities as subtotal_utilities
import utilities.outlines_utilities as outlines_utilities
import utilities.format_utilities as format_utilities
import utilities.column_names_utilities as cols

import xlsxwriter

from datetime import datetime

def format_ceo_review_report(df, format_config, ranking_config, sheet_name, file_name, dir_path):
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
    format_config: dict
        A dictionary of format configuration to be used for computing subtotals, applying outlines and formatting
        Eg: "format_config" : {
                "subtotal_outlines_dict" : {
                    "level_subtotal_cols_dict" : {"1" : "cols.deo_name_sec"},
                    "agg_cols_func_dict" : {
                        "cols.cwsn_tot": "sum",
                        "cols.nid_count": "sum",
                        "cols.udid_count": "sum",
                        "cols.deo_sec_rank": "mean"
                    },
                    "text_append_dict" : {"cols.deo_name_sec": "Summary"}
                },
                "format_dict" : {
                    "conditional_format" : {
                        "columns" : ["cols.perc_fully_mapped"],
                        "format": {"type": "3_color_scale"}
                    },
                    "format_cells" : {
                        "columns" : ["cols.perc_fully_mapped"],
                        "format" : {"num_format": "0.00%"}
        
                    }
                }
            }
    ranking_config: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        This dictionary contains the ranking_args dict, which will be mainly used to update the formatted data
        with ranking values/ranks
        Eg: ranking_args = {
                'ranking_type' : 'percent_ranking',
                'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
                'ranking_val_desc' : '% moved to CP',
                'num_col' : 'class_1',
                'den_col' : 'Total',
                'sort' : True,
                'ascending' : False
                }
    sheet_name: str
        The name of the sheet to save the data in.
    file_name: str
        The name of the file to save the data sheet in.
    dir_path: str
        The directory in which to save the file in.
    """

    # Get the subtotal and outlines specific configurations
    subtotal_outlines_dict = format_config['subtotal_outlines_dict']
    level_subtotal_cols_dict = subtotal_outlines_dict['level_subtotal_cols_dict']
    agg_cols_func_dict = subtotal_outlines_dict['agg_cols_func_dict']
    text_append_dict = subtotal_outlines_dict['text_append_dict']
    print("report format utilities:", df.columns)

    # Compute sub-totals and insert into provided dataframe
    subtotals_result_dict = subtotal_utilities.compute_insert_subtotals(df, subtotal_outlines_dict, ranking_config)

    # Get the updated DataFrame object - with the subtotals inserted
    updated_df = subtotals_result_dict['updated_df']
    # Get only the subtotal rows
    df_subtotal_rows = subtotals_result_dict['subtotals']

    # Get and update the data frame with a grand total row at the bottom of the data set  
    ranking_val_desc = ranking_config['ranking_args']['ranking_val_desc']
    agg_dict = ranking_config['ranking_args']['agg_dict']
    grand_total_row = _get_grand_total_row(df, agg_dict, ranking_val_desc)
    print('grand_total_row: ', grand_total_row)
    updated_df.loc['Grand Total'] = grand_total_row
    

    # Remove rank for rows other than subtotal rows - commented as this needs to be fixed
    #appended_col = list(text_append_dict.keys())[0]
    #if (appended_col == cols.deo_name_elm):
        #updated_df[~updated_df[appended_col].str.contains(text_append_dict[appended_col])][cols.deo_elem_rank] = ''
        #updated_df.loc[updated_df[~updated_df[appended_col].str.contains(text_append_dict[appended_col])] == True][cols.deo_elem_rank] = ''
        #updated_df[cols.deo_elem_rank] = np.where(~updated_df[appended_col].str.contains(text_append_dict[appended_col]), '', updated_df[cols.deo_elem_rank])

    # Build outlines levels and ranges dictionary
    level_outline_ranges_dict = outlines_utilities.build_level_outline_ranges_dict(
        updated_df, df_subtotal_rows, level_subtotal_cols_dict, agg_cols_func_dict)

    # Shift the outline ranges by 1 to accommodate the column headers
    level_outline_ranges_dict = outlines_utilities.push_outline_ranges_for_formatting(level_outline_ranges_dict, 1)

    
    # Shift the data by 1 row down - To create space for report heading
    #updated_df = updated_df.shift(periods=1, fill_value=0)

    # Extracting the column names for renaming
    col_names = updated_df.columns.to_list()
    # Checking if the report is elementary or secondary
    if col_names[0] == cols.deo_name_elm:
        updated_df.rename(columns={
            cols.deo_name_elm: cols.deo_name_elementary,
            cols.block_name: cols.block_name_output
        }, inplace=True
        )
    elif col_names[0] == cols.deo_name_sec:
        updated_df.rename(columns={
            cols.deo_name_sec: cols.deo_name_secondary,
            cols.block_name: cols.block_name_output
        }, inplace=True
        )

    # Update any other column names given to be renamed
    if 'columns_rename_dict' in format_config and bool(format_config['columns_rename_dict']):
        
        columns_rename_dict = cols.update_dictionary(format_config['columns_rename_dict'])
        updated_df.rename(columns=columns_rename_dict, inplace=True)

    # Drop any columns configured to be dropped
    if 'columns_to_drop' in format_config and bool(format_config['columns_to_drop']):
        cols_to_drop = cols.get_values(format_config['columns_to_drop'])
        updated_df.drop(columns=cols_to_drop, inplace=True)

    # Insert a blank row in the top of the data frame to write the heading
    # Get the number of columns in the data - to merge
    no_of_columns = len(updated_df.columns.to_list())

    # Insert a blank row to the top of the data frame
    row_to_insert = []
    for i in range (0, no_of_columns):
        row_to_insert.append(type(updated_df.columns[i])(0))
    updated_df = utilities.insert_row(updated_df, 0, row_to_insert)

    # Get the XlsxWriter object
    writer = file_utilities.get_xlsxwriter_obj({sheet_name: updated_df}, file_name, file_path=dir_path)

    # Get a XlsxWriter workbook and worksheet object
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name(sheet_name)
    
    # Apply the outlines function to the work sheet for the given levels and ranges
    outlines_utilities.apply_outlines(worksheet, level_outline_ranges_dict)

    # Insert heading
    # Get the heading to be inserted
    heading = format_config['heading']
    date = datetime.now().strftime('%d %h %y')
    full_heading = heading + ' - ' + date
    format_utilities.write_heading(updated_df, full_heading, worksheet, workbook)

    # Apply border to the entire data
    format_utilities.apply_border(updated_df, worksheet, workbook)

    # Apply formatting for columns as specified in the JSON configuration
    format_dicts_list = format_config['format_dicts']
    format_utilities.apply_formatting(format_dicts_list, updated_df, worksheet, workbook)

    # Apply formatting to the subtotal rows
    subtotal_row_indices = subtotals_result_dict['subtotal_row_indices']
    # Add 1 to the subtotal row indices as a heading row has been inserted at the top of the data
    subtotal_row_indices = [x + 1 for x in subtotal_row_indices]
    subtotal_utilities.format_subtotal_rows(worksheet, workbook, updated_df, subtotal_row_indices)

    # correct the formatting loss from applying subtotal row formatting
    subtotal_utilities.correct_col_formatting_loss(worksheet, workbook, updated_df, subtotal_row_indices, format_dicts_list)

    # Format the grand total row
    _format_grand_total_row(worksheet, workbook, updated_df)

    # correct the formatting loss in grand total row from applying grand total row formatting
    _correct_grand_total_col_frmt_loss(worksheet, workbook, updated_df, format_dicts_list)

    # Format the header
    format_utilities.format_col_header(updated_df, worksheet, workbook)

    # Save the formatted data
    writer.close()


def format_ad_hoc_report_and_save(df_reports, summary_sheets_args, file_name):
    """
    Function to prepare the add hoc report for viewing by applying the given 
    formatting configurations on the data.

    The function also saves the formatted data in the current day of the month
    folder in generated reports folder.

    Parameters:
    ----------
    df_reports: dict
        The ad hoc report summaries as a dictionary of Pandas DataFrame objects
    summary_sheets_args: dict
        Dictionary of arguments required to create summaries of data each of which 
        contains a dictionary of format configurations to be used to clean up the data 
        and apply visual formatting.
        Eg:
        "format_config" : {
                        "heading" : "Career Guidance 12th passout support required report",
                        "cols_to_drop": [],
                        "cols_rename_dict" : {
                            "cols.student_name" : "cols.cg_stu_appld"
                        },
                        "format_dicts" : [
                            {
                                "description" : "Apply percentage formatting",
                                "columns" : ["cols.cg_stu_appld"],
                                "format" : {"num_format": "0.00%"}
                            },
                            {
                                "description" : "Apply 3 colour gradient heatmap",
                                "columns" : ["cols.cg_stu_appld"],
                                "conditional_format_flag" : true,
                                "conditional_format" : {"type": "3_color_scale"}
                              }
                        ]
                    }
    file_name: str
        The file name to be used to save the data
    """

    # Create a summary sheet name - format configs dict
    summary_format_config_dict = {}
    for summary_sheet_args in summary_sheets_args:
        summary_format_config_dict[summary_sheet_args['summary_sheet_code']] = summary_sheet_args['format_config']

    # For each summary data in the dictionary, apply the formatting
    for sheet_name, df_summary in df_reports.items():

        # If sheet name is base report, skip the formatting
        if sheet_name == 'base_report':
            continue

        # Get the format configs for the sheet
        format_config = summary_format_config_dict[sheet_name]

        # Check for rename configuration and update
        if 'cols_rename_dict' in format_config and bool(format_config['cols_rename_dict']):
            columns_rename_dict = format_config['cols_rename_dict']
            df_summary.rename(columns=columns_rename_dict, inplace=True)

        # Drop any columns configured to be dropped
        if 'cols_to_drop' in format_config and bool(format_config['cols_to_drop']):
            cols_to_drop = format_config['cols_to_drop']
            df_summary.drop(columns=cols_to_drop, inplace=True)

    # Convert the dictionary of data frames to dictionary of xlsxwriter objects for formatting
    dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
    writer = file_utilities.get_xlsxwriter_obj(df_reports, file_name, dir_path)

    
    # Format and save the xlsxwriter objects
    for key in df_reports.keys():

        # Get the worksheet
        workbook = writer.book
        worksheet = workbook.get_worksheet_by_name(key)

        # Apply formatting for all sheets other than base_report
        if key != 'base_report':
            # Get the format dictionaries
            format_config = summary_format_config_dict[key] 
            format_dicts_list = format_config['format_dicts']

            # Apply border to the data
            format_utilities.apply_border(df_reports[key], worksheet, workbook)

            # Apply formatting specified in JSON
            format_utilities.apply_formatting(format_dicts_list, df_reports[key], worksheet, workbook, start_row=1)

            # Insert heading for the summary sheet 
            # TODO Probably need to insert a blank row in the data before getting the xlsx writer objects
            format_utilities.write_heading(df_reports[key], format_config['heading'], worksheet, workbook)

            # Format the header
            format_utilities.format_col_header(df_reports[key], worksheet, workbook)
    
        
    writer.save()        




def _get_grand_total_row(df, agg_dict, ranking_val_desc):
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
    
    grand_total_row[df.columns.get_loc(ranking_val_desc)] = df[ranking_val_desc].mean()

    return grand_total_row


def _format_grand_total_row(worksheet, workbook, df):
    """
    Internal helper function to format the Grand total row which will be the last row
    in the data

    Parameters:
    -----------
    worksheet: Worksheet
        An XlsxWriter worksheet object
    workbook: Workbook
        An XlsxWriter workbook object
    df: DataFrame
        The data containing the grand total row at the end
    """

    # Get the index of the last row
    row_index = df.shape[0]

    # Define the formatting to apply for all subtotal rows
    cell_format = workbook.add_format()
    # Set the subtotal rows to bold
    cell_format.set_bold() 
    # Set the subtotal row background to grey
    cell_format.set_bg_color('#d3d2d2')
    # Set the border for the subtotal row
    cell_format.set_border(1)
    # Set the alignment of the text
    cell_format.set_align('center')

    # Rewrite the grand total, but with formatting
    # Add 1 to row index location as report heading will have been inserted at the top
    worksheet.write_row(row_index, 0, df.iloc[row_index - 1], cell_format)


def _correct_grand_total_col_frmt_loss(worksheet, workbook, df, format_dicts_list):
    """
    Helper function to re-apply the column formatting previously applied
    and lost when the subtatol row is formatted.

    Parameters:
    ----------
    worksheet: Worksheet
        An XlsxWriter worksheet object
    workbook: Workbook
        An XlsxWriter workbook object
    df: DataFrame
        The data containing the grand total row at the end
    format_dicts_list: list
        List of dictionaries where each dictionary item contains list of columns to apply a formatting on
    """

    # Get the index of the last row
    row_index = df.shape[0]

    for format_dict in format_dicts_list:
    
        # Get the column name variables
        columns = format_dict['columns']
        # Get the resolved column name values
        columns = cols.get_values(columns)

        format = format_dict['format']

        # update format with the cell format
        #format.update(cell_format)
        cell_format = workbook.add_format(format)

        # Add the cell formats that were applied in subtotaling
        
        # Set the subtotal rows to bold
        cell_format.set_bold() 
        # Set the subtotal row background to grey
        cell_format.set_bg_color('#d3d2d2')
        # Set the border for the subtotal row
        cell_format.set_border(1)
        # Set the alignment of the text
        cell_format.set_align('center')

        # For each column
        for column in columns:
            
            col_index = df.columns.get_loc(column)
            # Rewrite the grand total row columns with lost formatting
            # Add 1 to row index location as report heading will have been inserted at the top
            worksheet.write(row_index, col_index, df.iloc[row_index-1, col_index], cell_format)
