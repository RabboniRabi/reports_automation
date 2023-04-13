"""
Module to clean the column names
"""


import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities
import pandas as pd
import re

def standardise_column_names(df_report):
    """
    The same column has different names in different data sets. This function matches such columns and applies standard
    columns names to:
    district_name, edu_dist_name, block_name, udise_code, school_name

    Parameters:
    ----------
    df_report: Pandas Dataframe
        The data whose column names are to be checked and renamed to standard format

    Returns:
    -------
        Dataframe object with the desired column names.
    """
    # Declare Regex patterns to match different types of names for the same column (for district, school, udise & block)
    dist_pattern = re.compile("(?i)^dist(([\s\S]|)name(?=s$|$)|$)|^dist(?:rict([\s\S]|)name(?=s$|$)|(?:rict)$)")
    edu_dist_pattern = re.compile("(?i)^edu(?:cation|)([\s\S]|)dist(?:rict|)(([\s\S]|)name(?=s$|$)|$)")
    school_name_pattern = re.compile(("(?i)^school([\s\S]|)name(?=s$|$)|^school(?=s$|$)"))
    udise_pattern = re.compile("(?i)^udise([\s\S]|)code(?=s$|$)|^udise$")
    block_pattern = re.compile("(?i)^block([\s\S]|)name(?=s$|$)|^block$|^blk([\s\S]|)(?:name(?=s$|$)|$)")

    # For each column in the list of column names in the given data
    for col_name in df_report.columns:
        # If column name matches district pattern, rename it to value in cols.district_name
        if re.search(dist_pattern, col_name):
            df_report.rename(columns={col_name: cols.district_name}, inplace=True)
        # If column name matches educational district pattern, rename it to value in cols.edu_district_name
        elif re.search(edu_dist_pattern, col_name):
            df_report.rename(columns={col_name: cols.edu_district_name}, inplace=True)
        # If column name matches school name pattern rename it to value in cols.school_name
        elif re.search(school_name_pattern, col_name):
            df_report.rename(columns={col_name: cols.school_name}, inplace=True)
        # If column name matches UDISE code pattern rename it to value in cols.udise_col
        elif re.search(udise_pattern, col_name):
            df_report.rename(columns={col_name: cols.udise_col}, inplace=True)
        # If column name matches block name pattern rename it to value in cols.block_name
        elif re.search(block_pattern, col_name):
            df_report.rename(columns={col_name: cols.block_name}, inplace=True)
        else:
            continue

def main():
    # Ask the user to select the excel file to clean the columns.
    report = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(report, sheet_name='Report', skiprows=4)
    # For testing
    column_cleaning(df_report)

if __name__ == "__main__":
    main()

