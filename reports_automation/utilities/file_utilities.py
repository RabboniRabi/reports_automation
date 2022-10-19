"""
Module with utility functions related to opening, reading and writing files
that can be commonly used across the project.
"""


import tkinter.filedialog as filedialog
import os
import sys

from pathlib import Path

def ask_open_file(file_types, initialdir):
    """
    Function to open a file open dialog and return the user file.

    Parameters:
    -----------
    file_types: array
        The file types to be opened
    initialdir: str
        The path to the initial directory to open the dialog in
    
    Returns:
    --------    
    File object with the opened file
    """
    file = filedialog.askopenfile(mode='r',initialdir=initialdir, filetypes=file_types)
    if file is not None:
        return file
    else:
        sys.exit('No file selected!')


def open_excel():
    """
    Function to open excel files by user
    """
    initialdir = get_download_dir_path()
    filetypes =[('Excel files', '*.xlsx')]
    return ask_open_file(filetypes, initialdir)

def open_scripts():
    """
    Function to open script files by user
    """
    initialdir = str(os.path.join(Path.cwd(), "scripts"))
    filetypes =[]
    return ask_open_file(filetypes, initialdir)    

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
    file_path = os.path.join(os.getcwd(), '../', 'sql_scripts', script_file_name)

    file = open(file_path,'r')

    return file

def get_download_dir_path():
    """
    Function to get the path to the downloads directory in the OS.
    The function should work for all Operating Systems
    """
    return str(os.path.join(Path.home(), "Downloads"))

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
    Function to save a data frame to excel - not complete

    Parameters:
    ----------
    df_sheet_dict: dictionary
        A dictionary containing sheet-dataframe key-value paits
    file_name: str
        File name to save the data in
    index: bool
        Boolean value indicating if row names need to be written. Default is False

    """
    curr_dir = os.getcwd()
    output_data_path = '../../../reports/generated/'
    file_path = os.path.join(curr_dir, output_data_path, file_name)
    datatoexcel = pd.ExcelWriter(file_path)
    for key in df_sheet_dict:
        df_sheet_dict[key].to_excel(datatoexcel, sheet_name=key, index=index)
        print('Saving ', key, ' sheet in excel file: ', file_name, '....')
    datatoexcel.save()
    print('Save done')