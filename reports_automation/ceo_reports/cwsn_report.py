"""
Module to use the CWSN report available in the dashboard to create a report with
 - Block wise count of students with NID
 - Block wise count of students with UDID
 - Block wise count of total students
 - Block wise count of students attending schools
 - Block wise count of students attending SRPs (IE) centres
 - Block wise count of home based students
"""


import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.utilities as utilities
import pandas as pd
import numpy as np


def get_grouping_level_wise_student_count(df, group_levels, student_count_col):
    """
    Function to get the grouping levels wise count of CWSN students

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    student_count_col: str
        The column to count
    Returns:
    --------
    DataFrame object with group level wise count of total CWSN students
    """

    df_grouped = df.groupby(group_levels,sort=False)[student_count_col].count().reset_index()

    df_grouped.rename(columns={student_count_col: 'Total CWSN Students'}, inplace=True)

    return df_grouped

def get_grouping_level_wise_IDs_issued_count(df, group_levels, id_columns):
    """
    Function to get the grouping levels wise count of students with disability IDs.

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    id_columns: list
        The name of columns with IDs that need to be counted        
    Returns:
    --------
    DataFrame object with group level wise count of students with disability ids
    """

    # Drop missing values in IDs
    df = df.dropna(subset=id_columns)

    accepted_values_regex = '[1-9].|TN.' # A regex with the accepted range/type of values

    df_filtered_grouped = utilities.filter_group_count_valid_values(df, group_levels, id_columns, accepted_values_regex)

    return df_filtered_grouped

def get_grouping_level_wise_supported_cat_count(df, group_levels, supp_cats, supp_cat_column):
    """
    Function to get the count of support provided in different categories 
    at each grouping level.

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    supp_cats: list
        The supported categories of schooling
    supp_cap_column: str
        The column with details of support category for student    
    Returns:
    --------
    DataFrame object with count of support provided in different categories
    """

    # Pivot the table and count the number of different categories in 'SupportedIn' column
    df_pivot = pd.pivot_table(df, index=group_levels, columns=supp_cat_column,
                aggfunc='size', fill_value=0, sort=False).reset_index()

    # Filter the result of the pivot with columns containing grouping levels and supported categories
    selected_columns = group_levels + supp_cats            

    df_supp_cat_count = df_pivot[selected_columns]

    return df_supp_cat_count


def main():

    # Read report from excel
    df_report = pd.read_excel(r'/home/rabboni/Downloads/CWSN-Report.xlsx', sheet_name='Report', skiprows=4)

    # List of columns with student IDs
    id_columns = ['NID', 'UDID']
    # Levels to apply grouping by
    group_levels = ['District', 'Edu_District', 'Block']
    # List of places student is supported in
    supp_cats = ['School', 'SRP Center', 'Home Based']

    # Get block level wise total students count
    block_wise_total_students_count = get_grouping_level_wise_student_count (df_report, group_levels, 'Name')
    # Get block level wise count of valid student IDs
    block_wise_IDs_issued_count = get_grouping_level_wise_IDs_issued_count(df_report, group_levels, id_columns)
    # Get block level wise count of supported categories
    block_wise_supp_cat_wise_count = get_grouping_level_wise_supported_cat_count(
        df_report, group_levels, supp_cats, 'SupportedIn')
    
    # Merge the results into one block level summary
    df_overview = block_wise_total_students_count.merge(block_wise_IDs_issued_count[group_levels+id_columns])
    df_overview = df_overview.merge(block_wise_supp_cat_wise_count[group_levels+supp_cats])

    # Rename columns for better readability
    df_overview.rename(columns = {
        'NID':'NID count',
        'UDID':'UDID count',
        'School':'Students at Schools',
        'SRP Center':'Students at SRP Centers',
        'Home Based': 'Home Based Students'
        }, inplace = True)

    file_utilities.save_to_excel({'Report':df_overview}, 'CWSN_Summary.xlsx')



if __name__ == "__main__":
    main()