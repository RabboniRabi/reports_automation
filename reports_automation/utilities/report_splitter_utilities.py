"""
Module to filter based on a specific column value and save in separate files
"""

import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols
import os



def split_report(df_report, column_to_split_on):
    """
    Function to split the given data on a given column and update the dataframe in a dictionary
    Args:
        df_report: Data to split
        column_to_split: column name to split the data on


    Returns:
    Filtered dictionary
    """
    column_unique_values = df_report[column_to_split_on].unique()
    # Creating an empty dictionary
    split_data_dict = {}
    # Loop to filter the unique values in a dataframe bases on a specific column
    for col_value in column_unique_values:
        df_filtered = df_report[df_report[column_to_split_on] == col_value]
        # Updating the filtered dataframe in a dictionary
        split_data_dict.update({col_value: df_filtered})

    return split_data_dict

def save_split_report(split_df_data):
    """
    Function to save the multiple dataframes in a dictionary to an Excel files
     Parameters
        ---------
        split_df_data:
    """
    # Loop to iterate through dictionary for saving in separate files
    for key in split_df_data.keys():

        dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
        file_utilities.save_to_excel({'Report': split_df_data[key]}, key + '.xlsx', dir_path=dir_path)


def split_report_given_file(file_name, column_to_split_on, sheet_name, skiprows=0):
    """
        Function to only split the given data and save it in separate files if there is no custom configurations

        Parameters
        ---------
        file_name: Source data excel file
        column_to_split_on: column name to split the data on
        sheet_name: which worksheet to use

        """


    dir_path = file_utilities.get_curr_month_source_data_dir_path()
    file_path = os.path.join(dir_path, file_name)
    df = file_utilities.read_sheet(file_path, sheet_name, skiprows)

    split_data_set = split_report(df, column_to_split_on)

    save_split_report(split_data_set)


