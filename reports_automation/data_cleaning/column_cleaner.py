"""
Module to clean the column names
"""


import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities
import pandas as pd
import re

def column_cleaning(df_report):
    """
    Function to clean the column names by finding the patterns and replacing it with our desired column names.
    Parameters:
    ----------
        df_report: Pandas Dataframe

    Returns:
        Dataframe object with the desired column names.

    """
    # Declaring the patterns
    dist_pattern = re.compile("(?i)^dist(([\s\S]|)name(?=s$|$)|$)|^dist(?:rict([\s\S]|)name(?=s$|$)|(?:rict)$)")
    edu_dist_pattern = re.compile("(?i)^edu(?:cation|)([\s\S]|)dist(?:rict|)(([\s\S]|)name(?=s$|$)|$)")
    school_name_pattern = re.compile(("(?i)^school([\s\S]|)name(?=s$|$)|^school(?=s$|$)"))
    udise_pattern = re.compile("(?i)^udise([\s\S]|)code(?=s$|$)|^udise$")
    block_pattern = re.compile("(?i)^block([\s\S]|)name(?=s$|$)|^block$|^blk([\s\S]|)(?:name(?=s$|$)|$)")

    # Loop for checking the column names
    for col_name in df_report.columns:
        if re.search(dist_pattern, col_name):
            df_report.rename(columns={col_name: cols.district_name}, inplace=True)
        elif re.search(edu_dist_pattern, col_name):
            df_report.rename(columns={col_name: cols.edu_district_name}, inplace=True)
        elif re.search(school_name_pattern, col_name):
            df_report.rename(columns={col_name: cols.school_name}, inplace=True)
        elif re.search(udise_pattern, col_name):
            df_report.rename(columns={col_name: cols.udise_col}, inplace=True)
        elif re.search(block_pattern, col_name):
            df_report.rename(columns={col_name: cols.block_name}, inplace=True)
        else:
            continue
    return df_report

def main():
    # Ask the user to select the excel file to clean the columns.
    report = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(report, sheet_name='Report', skiprows=4)
    # For testing
    column_cleaning(df_report)

if __name__ == "__main__":
    main()

