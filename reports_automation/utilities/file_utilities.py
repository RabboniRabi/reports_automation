"""
Module with utility functions related to opening, reading and writing files
that can be commonly used across the project.
"""

import os
import sys
import pandas as pd

from easygui import fileopenbox
from pathlib import Path
from datetime import datetime

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
    try:
        curr_dir_path = Path(os.getcwd())
        file_path = os.path.join(curr_dir_path.parents[0], 'sql_scripts', script_file_name)

        file = open(file_path,'r')
    except OSError as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            err_msg = 'Unable to open file: ' + script_file_name 
            sys.exit(err_msg)
    return file

def get_download_dir_path():
    """
    Function to get the path to the downloads directory in the OS.
    The function should work for all Operating Systems

    Returns:
    --------
    The path to the user's download path
    """
    return os.path.join(Path.home(), 'Downloads')

def get_reports_dir_path():
    """
    Function to get the path to the folder where all generated reports, 
    mapping data and source data for reports are stored
    Returns:
    -------
    The path to the reports folder
    """    
    curr_dir_path = Path(os.getcwd())
    # Get the path to parent three levels up
    parent_dir_three_lvls_up = curr_dir_path.parents[2]
    dir_path = os.path.join(parent_dir_three_lvls_up, 'reports')
    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)
    return dir_path


def get_gen_reports_dir_path():
    """
    Function to get the path to the folder where generated reports are to be saved.

    Returns:
    -------
    The path to the generated reports folder
    """    

    dir_path = os.path.join(get_reports_dir_path(), 'generated')
    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)
    return dir_path

def get_adw_data_dir_path():
    """
    Function to get the path to the folder where source data is saved.

    Returns:
    -------
    The path to the source data folder
    """

    dir_path = os.path.join(get_gen_reports_dir_path(), 'adw_data_extraction')
    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)
    return dir_path

def get_mapping_data_dir_path():
    """
    Function to get the path to the folder where mapping data is saved.

    Returns:
    -------
    The path to the mapping data folder
    """    

    dir_path = os.path.join(get_reports_dir_path(), 'mapping_data')
    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)
    return dir_path

def get_source_data_dir_path():
    """
    Function to get the path to the folder where source data is saved.

    Returns:
    -------
    The path to the source data folder
    """    

    dir_path = os.path.join(get_reports_dir_path(), 'source_data')
    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)
    return dir_path

def get_curr_month_source_data_dir_path():
    """
    Function to get the directory path to the current month's source data.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the current month's source data directory
    """
    # Get the current month and year
    curr_month_year = datetime.now().strftime('%h_%y')
    dir_path = os.path.join(get_source_data_dir_path(), curr_month_year)

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path

def get_curr_month_gen_reports_dir_path():
    """
    Function to get the directory path to the current month's generated reports.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the current month's generated reports directory
    """
    # Get the current month and year
    curr_month_year = datetime.now().strftime('%h_%y')
    dir_path = os.path.join(get_gen_reports_dir_path(), curr_month_year)

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path

def get_curr_day_month_gen_reports_dir_path():
    """
    Function to get the directory path to the current day's generated reports.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the current month's generated reports directory
    """
    # Get the current month and year
    curr_day_month = datetime.now().strftime('%d_%h')
    dir_path = os.path.join(get_curr_month_gen_reports_dir_path(), curr_day_month)

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path

def get_curr_day_month_gen_report_name_dir_path(dir_name):
    """
     Function to get the directory path to the specified directory name in current day's generated reports.
      The function also creates the directory if it does not already exist.
    Args:
        dir_name: The name of the folder want to store the excel files.

    Returns:
    -------
    The path to the current month's specified directory name in generated reports directory
    """
    dir_path = os.path.join(get_curr_day_month_gen_reports_dir_path(), dir_name)

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path


def get_ceo_rpts_dir_path():
    """
    Function to get the directory path to CEO reports folder.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the CEO reports directory
    """
    dir_path = os.path.join(get_gen_reports_dir_path(), 'ceo_reports')
    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path

def get_curr_month_ceo_rpts_dir_path():
    """
    Function to get the directory path with the current month's ceo reports.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the current month's CEO reports directory
    """
    # Get the current month and year
    curr_month_year = datetime.now().strftime('%h_%y')
    dir_path = os.path.join(get_ceo_rpts_dir_path(), curr_month_year)

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path

def get_curr_month_elem_ceo_rpts_dir_path():
    """
    Function to get the directory path to the current month's Elementary level ceo reports.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the current month's CEO reports directory
    """
    dir_path = os.path.join(get_curr_month_ceo_rpts_dir_path(), 'Elementary')

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path    

def get_curr_month_secnd_ceo_rpts_dir_path():
    """
    Function to get the directory path to the current month's Secondary level ceo reports.
    The function also creates the directory if it does not already exist.

    Returns:
    -------
    The path to the current month's CEO reports directory
    """
    dir_path = os.path.join(get_curr_month_ceo_rpts_dir_path(), 'Secondary')

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path   

def get_ranking_reports_dir():
    """
    Function to get the directory path to the folder containing the ranking related reports

    Returns:
    -------
    The path to the progress report files directory
    """
    dir_path = os.path.join(get_ceo_rpts_dir_path(), 'ranking')

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path


def get_progress_reports_dir():
    """
    Function to get the directory path to the folder containing the progress reports:
    Reports that compare current performance to previous performance

    Returns:
    -------
    The path to the progress report files directory
    """
    dir_path = os.path.join(get_ranking_reports_dir(), 'progress_reports')

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path

def get_cons_ranking_reports_dir():
    """
    Function to get the directory path to the folder containing
    consolidated ranking reports.

    Returns:
    -------
    The path to the consolidated report files directory
    """
    dir_path = os.path.join(get_ranking_reports_dir(), 'consolidated_ranking')

    # If directory does not exist
    if not os.path.isdir(dir_path):
        create_dir(dir_path)

    return dir_path



def create_dir(dir_path):
    """
    Function to create a directory with the given directory path
    """
    # If directory does not exist
    if not os.path.isdir(dir_path):
        try:
            # Make directory
            os.makedirs(dir_path)
        except OSError:
            print(OSError)
        # Check that directory has been created
        if not os.path.isdir(dir_path):
            raise

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
        
def file_exists(file_name: str, dir_path:str):
    """
    Function to check if a given file name exists in a given directory path.

    Parameters:
    -----------
    file_name: str
        The name of the file whose existence has to be checked
    dir_path: str
        The path to the directory where the file existence needs to be checked

    Returns:
    --------
    True if file exists. False otherwise.
    """
    file_path = os.path.join(dir_path, file_name)

    file_exists = os.path.isfile(file_path)

    return file_exists

def build_dir_path(dir_levels:list):
    """
    Function to build an OS independent absolute path to a directory
    anywhere in the project
    Parameters:
    -----------
    dir_levels: list
        The list of successive directories from the root of the project
        upto to the final directory
    Returns:
    --------
    The full path to the directory
    """

    curr_dir_path = Path(os.getcwd())
    # Get the path to project root directory
    root_dir = curr_dir_path.parents[0]
    # Assign the full directory path initially to the root directory path and then update
    dir_path = root_dir
    for dir in dir_levels: 
        dir_path = os.path.join(dir_path, dir)

    return dir_path


def build_file_path(file_name: str, dir_levels:list):
    """
    Function to build a OS independent absolute path to a file 
    anywhere in the project
    Parameters:
    -----------
    file_name: str
        The name of the file whose full path has to be built
    dir_levels: list
        The list of successive directories from the root of the project
        upto to the directory containing the file
    Returns:
    --------
    The full path to the file
    """
    # Get the path to the directory
    dir_path = build_dir_path(dir_levels)

    file_path = os.path.join(dir_path, file_name)

    return file_path

def get_file_path(file_name: str, dir_path:str):
    """
    OS independent function to append file name to directory path
    and return the full file path.
    Parameters:
    -----------
    file_name: str
        The name of the file whose full path has to be retrieved
    dir_path: str
        The path to the directory where the file exists

    Returns:
    --------
    The full path to the file
    """
    file_path = os.path.join(dir_path, file_name)

    if(not os.path.isfile(file_path)):
        print('File: ', file_name, ' does not exist in ', dir_path)
        sys.exit('File does not exist in given directory')

    return file_path

def save_to_excel(df_sheet_dict, file_name, dir_path = get_gen_reports_dir_path(), index=False, engine='openpyxl'):
    """
    Function to save a data frame to excel using openpyxl engine

    Parameters:
    ----------
    df_sheet_dict: dictionary
        A dictionary containing sheet-dataframe key-value pairs
    file_name: str
        File name to save the data in
    dir_path: str, optional
        The directory path to save the file in. Default is the generated reports directory path
    index: bool, optional
        Boolean value indicating if row names need to be written. Default is False
    engine: str
        The name of the Excel engine to be used. xlsxwriter or openpyxl. Default is openpyxl.
    """
    file_path = os.path.join(dir_path, file_name)
    datatoexcel = pd.ExcelWriter(file_path, engine=engine)
    for key in df_sheet_dict.keys():
        df_sheet_dict[key].to_excel(datatoexcel, sheet_name=key, index=index)
        print('Saving ', key, ' sheet in excel file: ', file_name, '....')
    datatoexcel.close()
    print('Save done')


def get_xlsxwriter_obj(df_sheet_dict, file_name, file_path = get_gen_reports_dir_path(), index=False,start_row=0, start_col=0):
    """
    Function to convert the Pandas DataFrame object to 
    a ready to use and save XlsxWriter object.

    Parameters:
    ----------
    df_sheet_dict: dictionary
        A dictionary containing sheet-dataframe key-value pairs
    file_name: str
        File name to save the data in
    file_path: str, optional
        The directory path to save the file in. Default is generated reports directory path    
    index: bool
        Boolean value indicating if row names need to be written. Default is False
    start_row: int
        Integer value indicating the which row the dataframe will be printed in
    start_col: int
        Integer value indicating the which column the dataframe will be printed in

    Returns:
    -------
    An XlsxWriter object    
    """

    file_path = os.path.join(file_path, file_name)
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    for key in df_sheet_dict.keys():
        df_sheet_dict[key].to_excel(writer, sheet_name=key, index=index,startrow=start_row,startcol=start_col)
    return writer


def get_xlsxwriter_objs(df_dict, dir_path=get_curr_day_month_gen_report_name_dir_path, index=False,start_row=0, start_col=0):
    """
    Function to convert the Pandas DataFrame objects in the given dictionary 
    to a ready to use and save dictionary of XlsxWriter objects to be saved
    in the given directory path.

    Parameters:
    ----------
    df_dict: dictionary
        A dictionary of key-name, value-data frame pairs
    dir_path: str, optional
        The directory path to save the file in. Default is current day, month generated reports directory   
    index: bool
        Boolean value indicating if row names need to be written. Default is False
    start_row: int
        Integer value indicating the which row the dataframe will be printed in
    start_col: int
        Integer value indicating the which column the dataframe will be printed in

    Returns:
    -------
    Dictionary of XlsxWriter objects    
    """
    # Declare a dictionary of xlsxwriter objects
    xlsxwriters_dict = {}

    # Iterate through the data frames and get the corresponding xlsxwriter objects
    for key in df_dict.keys():
        df = df_dict[key]
        xlsxwriters_dict[key] = get_xlsxwriter_obj({key:df}, str(key).title()+'.xlsx', dir_path, index, start_row, start_col)

    return xlsxwriters_dict


