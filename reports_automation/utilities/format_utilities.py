"""
Module with utility functions to apply formatting on data using the XlsxWriter library
"""

import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols

import xlsxwriter


def apply_cond_frmt(writer: xlsxwriter, sheet_name, col_index, cond_frmt_dict, no_of_rows):
    """
    Function to apply conditional formatting on given data and return
    the formatted xlsxwriter object

    Parameters:
    ----------
    writer: xlsxwriter
        The data as a xlsxwriter object
    sheet_name: str
        The name of the excel sheet where column to format is    
    col_index: int
        The index of the column on which to apply the formatting
    cond_frmt_dict: dict
        The conditional format to be applied on the column range
        eg: {'type': '3_color_scale'}
        eg: {
            'type': 'cell', 'criteria': 'greater than',
             'value': 5, 'format': red_format
            }
    no_of_rows: int
        The number of data rows
    """
    worksheet = writer.sheets[sheet_name]

    # Get the excel alphabet for the column. 
    col_excel_alphabet = xlsxwriter.utility.xl_col_to_name(col_index)

    # Create a range from the row 1 (omit 0 as it contains the header) of the column 
    # to the last row of the column. Adding a 1 as formatting seems to be applyed to last row -1.
    cells_range = col_excel_alphabet + str(1) + ':' + col_excel_alphabet + str(no_of_rows + 1)

    # Apply the conditional formatting on the entire column
    worksheet.conditional_format(cells_range, cond_frmt_dict)

def apply_frmt_col(worksheet, workbook, col_index, df, format_dict, width=None):
    """
    Apply a given formatting to a column in xlsxwriter Worksheet object
    
    Parameters:
    ----------
    worksheet: Worksheet
        An XlsxWriter Worksheet object
    workbook: Workbook
        An XlsxWriter Workbook object  
    col_index: int
        The index of the column on which to apply the formatting
    df: DataFrame
        Data as an instance of Pandas DataFrame object
    format_dict: dict
       A dictionary of format properties to be applied
        eg: {'bold': True, 'font_color': 'red'}
    width: float
        The width of the column(s)
    """

    # Get the format dictionary as an xlsxwriter Format object
    format_obj = workbook.add_format(format_dict)

    # Re-write the data in the given column along with the given formatting
    worksheet.write_column(1, col_index, df.iloc[:,col_index], format_obj)

def apply_frmt_cols (worksheet, workbook, start_col_index, end_col_index, format_dict, width=None, no_of_rows=None):
    """
    Apply a given formatting to a continguous range of columns in the given sheet in the given xlsxwriter object
    
    Parameters:
    ----------
    worksheet: Worksheet
        An XlsxWriter Worksheet object
    workbook: Workbook
        An XlsxWriter Workbook object    
    start_col_index: int
        The index of the starting column on which to apply the formatting
    end_col_index: int
        The index of the ending column on which to apply the formatting
    format_dict: dict
        The conditional format to be applied on the column range
        eg: {'type': '3_color_scale'}
        eg: {
            'type': 'cell', 'criteria': 'greater than',
             'value': 5, 'format': red_format
            }
    width: float
        The width of the column(s). Default is None
    no_of_rows: int
        The number of rows to apply the columns formatting. Default is None - Will apply for all columns.
    """

    # Get the format dictionary as an xlsxwriter Format object
    format_obj = workbook.add_format(format_dict)
    
    # Get the excel alphabets for the columns range
    start_col_excel_alphabet = xlsxwriter.utility.xl_col_to_name(start_col_index)
    end_col_excel_alphabet = xlsxwriter.utility.xl_col_to_name(end_col_index)
    # Create the column range
    if (no_of_rows is not None):
        # Create a range from the row 1 to no_of_rows+1 (Header starts at row 0, hence
        # row indexing gets shifted one place down.
        col_excel_alphabet_range = start_col_excel_alphabet + str(1) + ':' + end_col_excel_alphabet + str(no_of_rows + 1)
        print('col_excel_alphabet_range: ', col_excel_alphabet_range)
    else:
        col_excel_alphabet_range = start_col_excel_alphabet + ':' + end_col_excel_alphabet

    worksheet.set_column(col_excel_alphabet_range, width, format_obj)


def format_col_to_percent_and_save(df, column_name, sheet_name, file_name, dir_path):
    """
    Helper function to format a given column to percentage format and save the data.

    This function should ideally in simplifying formatting to percent and saving process.
    
    Parameters:
    ----------
    df: Pandas DataFrame
        The data with the column to be formatted
    column_name: str
        The name of the column to be formatted to perentage values
    sheet_name: str
        The name of the sheet to save the data in.
    file_name: str
        The name of the file to save the data sheet in.
    dir_path: str
        The directory in which to save the file in.
    """
    
    # Get an xlsx writer object of the data
    writer = file_utilities.get_xlsxwriter_obj({sheet_name: df}, file_name, file_path=dir_path)

    # Format values to percent
    prcnt_frmt = {'num_format': '0.00%'}

    # Get the index of the column to be formatted in the dataframe
    col_index = df.columns.get_loc(column_name)

    # Apply the formatting to the data
    apply_frmt_cols(writer, sheet_name, col_index, col_index, prcnt_frmt)

    # Save the data
    writer.save()


def apply_formatting(format_dicts_list, df, worksheet, workbook):
    """
    Function to apply formatting for each list of columns in a given 
    list of formatting dictionaries.

    Parameters:
    -----------
    format_dicts_list: list
        List of formatting dictionaries where each item contains a list of columns
        to apply the formatting on and the format to apply.
        Eg: [
                {
                    "columns" : ["cols.perc_students_with_acct"],
                    "format": {"type": "3_color_scale"}
                },
                {
                    "columns" : ["cols.perc_students_with_acct"],
                    "format" : {"num_format": "0.00%"}
                }
            ]
    df: DataFrame
        Data as an instance of Pandas DataFrame object
    worksheet: Worksheet
        An XlsxWriter worksheet object
    workbook: Workbook
        An XlsxWriter workbook object
    """
    # Define the base formatting that needs to be presisted for all cells
    common_format = {'align' : 'center', 'border' : 3}

    for format_dict in format_dicts_list:
        
        # Get the column name variables
        columns = format_dict['columns']
        # Get the resolved column name values
        columns = cols.get_values(columns)

        format = format_dict['format']

        # Update the given format with the common format, 
        #so that the common formatting is not lost.
        format.update(common_format)

        # For each column, get the index and call apply_frmt_col 
        # to apply formatting for that column
        for column in columns:
            
            col_index = df.columns.get_loc(column)

            apply_frmt_col(worksheet, workbook, col_index, df, format)


def insert_heading(df, worksheet, workbook):
    """
    Funtion to create a header at the top of the data

    Parameters:
    -----------
    df: DataFrame
        Data as an instance of Pandas DataFrame object
    worksheet: Worksheet
        An XlsxWriter worksheet object
    workbook: Workbook
        An XlsxWriter workbook object
    """

    # Get the number of columns in the data - to merge
    no_of_columns = len(df.columns.to_list())

    # Define the merge format
    merge_format = workbook.add_format({'align': 'center', 'bold': True})

    # Merge the cells to form the heading
    #worksheet.merge_range(0, 0, 0, no_of_columns - 1, 'merged row', merge_format)


def apply_border(df, worksheet, workbook):
    """
    Function to apply cell border to all cells in the data

    Parameters:
    ----------
    df: DataFrame
        Data as an instance of Pandas DataFrame object
    worksheet: Worksheet
        An XlsxWriter worksheet object
    workbook: Workbook
        An XlsxWriter workbook object
    """
    # Define the format to apply for all cells
    cell_format =  workbook.add_format({'align': 'center', 'border': 3})

    # Get the number of rows in the data
    no_of_rows = df.shape[0]

    # Write the format to each row in the data
    for i in range(1, no_of_rows):
        worksheet.write_row(i, 0, df.iloc[i-1], cell_format)


def format_col_header(df, worksheet, workbook):
    """
    Function to apply formatting for column header
    """
    # Define the format to apply for all cells
    cell_format =  workbook.add_format({'align': 'center', 'border': 1, 'bold': True, 'bg_color':'#808080'})

    # Format the header
    worksheet.write_row(0, 0, df.columns.to_list(), cell_format)
