"""
Module with utility functions related to opening, reading and writing files
that can be commonly used across the project.
"""

import os
import sys
import pandas as pd

from easygui import fileopenbox
from pathlib import Path

def ask_open_filename(file_types, initialdir):
    """
    Function to open a file open dialog and return the user selected filename.

    Parameters:
    -----------
    file_types: array
        The file types to be opened
    initialdir: str
        The path to the initial directory to open the dialog in
    
    Returns:
    --------    
    The name of the user selected file
    """
    filename = fileopenbox(default=initialdir, filetypes=file_types)
    if filename is not None:
        return filename
    else:
        sys.exit('No file selected!')


def user_sel_excel_filename():
    """
    Function to get the filename of the user selected excel file.
    
    Returns:
    -------
    The name of the user selected excel file
    """
    initialdir = get_download_dir_path()
    filetypes =[['*.xlsx', 'Excel files']]
    return ask_open_filename(filetypes, initialdir)

def open_scripts():
    """
    Function to get the file name of the user selected sql script file
    
    Returns:
    -------
    The name of the user selected excel file
    """
    initialdir = str(os.path.join(Path.cwd(), "sql_scripts"))
    filetypes = [['*.sql', 'SQL scripts']]
    return ask_open_filename(filetypes, initialdir)    

def open_script(script_file_name):
    """
    Function to open the sql script in a given file name.
    The function only searches in the sql_scripts directory
    
    Parameters:
    ----------
    script_file_name: str
        The name of the sql script file to open
    Returns:
    -------
    """
    curr_dir_path = Path(os.getcwd())
    file_path = os.path.join(curr_dir_path.parents[0], 'sql_scripts', script_file_name)

    file = open(file_path,'r')

    return file

def get_download_dir_path():
    """
    Function to get the path to the downloads directory in the OS.
    The function should work for all Operating Systems

    Returns:
    --------
    The path to the user's download path
    """
    return str(os.path.join(Path.home(), 'Downloads'))

def get_gen_reports_dir_path():
    """
    Function to get the path to the folder where generated reports are to be saved.

    Retunrs:
    -------
    The path to the generated reports folder
    """    
    curr_dir_path = Path(os.getcwd())
    # Get the path to parent three levels up
    parent_dir_three_lvls_up = curr_dir_path.parents[2]
    file_path = os.path.join(parent_dir_three_lvls_up, 'reports', 'generated')
    return file_path

def read_sheet(file_path, sheet_name, skiprows=0):
    """
    Function to read an excel sheet in a given excel file as a Pandas DataFrame object
    
    Parameters:
    ----------
    file_path: str
        The full file path that will be used to read the excel file
    sheet_name: str
        The name of the sheet within the excel file to read
    skiprows: int
        The number of rows to skip from the top. Default value is 0.
    Returns:
    -------
    Return a Pandas DataFrame object of the excel sheet read            
    """
    print('Loading ', sheet_name, 'sheet in ', file_path, ' as a data frame object...')
    data_frame = pd.read_excel(file_path, sheet_name, skiprows=skiprows)
    if data_frame is None and not data_frame.empty:
        sys.exit('Not able to load data frame')
    if (data_frame.empty):
        sys.exit('The data frame object is empty. Most likely, the sheet is empty')    
    else:
        print('Loading done.')
        return data_frame
        


def save_to_excel(df_sheet_dict, file_name, index=False):
    """
    Function to save a data frame to excel using openpyxl engine

    Parameters:
    ----------
    df_sheet_dict: dictionary
        A dictionary containing sheet-dataframe key-value paits
    file_name: str
        File name to save the data in
    index: bool
        Boolean value indicating if row names need to be written. Default is False

    """
    file_path = os.path.join(get_gen_reports_dir_path(), file_name)
    datatoexcel = pd.ExcelWriter(file_path, engine='openpyxl')
    for key in df_sheet_dict.keys():
        df_sheet_dict[key].to_excel(datatoexcel, sheet_name=key, index=index)
        print('Saving ', key, ' sheet in excel file: ', file_name, '....')
    datatoexcel.save()
    print('Save done')


def get_xlsxwriter_obj(df_sheet_dict, file_name, index=False):
    """
    Function to convert the Pandas DataFrame object to 
    a ready to use and save XlsxWriter object.

    Parameters:
    ----------
    df_sheet_dict: dictionary
        A dictionary containing sheet-dataframe key-value paits
    file_name: str
        File name to save the data in
    index: bool
        Boolean value indicating if row names need to be written. Default is False

    Returns:
    -------
    An XlsxWriter object    
    """

    file_path = os.path.join(get_gen_reports_dir_path(), file_name)
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    for key in df_sheet_dict.keys():
        df_sheet_dict[key].to_excel(writer, sheet_name=key, index=index)        
    return writer    