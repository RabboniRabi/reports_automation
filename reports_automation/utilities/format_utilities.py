"""
Module with utility functions to apply formatting on data using the XlsxWriter library
"""

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
    col_range = col_excel_alphabet + str(1) + ':' + col_excel_alphabet + str(no_of_rows + 1)

    # Apply the conditional formatting on the entire column
    worksheet.conditional_format(col_range, cond_frmt_dict)

def apply_frmt_cols (writer: xlsxwriter, sheet_name, start_col_index, end_col_index, format_dict, width=None):
    """
    Apply a given formatting to a continguous range of columns in the given sheet in the given xlsxwriter object
    
    Parameters:
    ----------
    writer: xlsxwriter
        The data as a xlsxwriter object
    sheet_name: str
        The name of the excel sheet where column to format is    
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
        The width of the column(s)
    """

    # Get the format dictionary as an xlsxwriter Format object
    workbook  = writer.book
    format_obj = workbook.add_format(format_dict)
    
    worksheet = writer.sheets[sheet_name]

    # Get the excel alphabets for the columns range
    start_col_excel_alphabet = xlsxwriter.utility.xl_col_to_name(start_col_index)
    end_col_excel_alphabet = xlsxwriter.utility.xl_col_to_name(end_col_index)
    # Create the column range
    col_excel_alphabet_range = start_col_excel_alphabet + ':' + end_col_excel_alphabet

    worksheet.set_column(col_excel_alphabet_range, width, format_obj)

