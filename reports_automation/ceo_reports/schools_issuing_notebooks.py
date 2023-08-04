"""
Module with custom functions to create students receiving notebooks report.
"""

import sys
sys.path.append('../')

import pandas as pd
import numpy as np

import utilities.column_names_utilities as cols

# Intial level to group the data to at pre-processing stage
initial_group_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.cate_type]

def _get_notebooks_issue_status_summary(df_data, grouping_cols):
    """
    Internal function to get summary of schools' notebooks issue statuses at grouping level

    Parameters:
    ----------
    df_data: Pandas DataFrame
        The notebooks issued status data to work on
    grouping_cols: list
        The list of columns to group by

    Returns:
    --------
    The summary of schools' notebooks issue statuses at grouping level
    """

    # Get issue status wise count of schools at grouping level
    data_pivot = pd.pivot_table(df_data, values=cols.udise_col, \
                        index=grouping_cols,columns=[cols.scheme_status], aggfunc='count',fill_value=0).reset_index()


    # Get the total number of schools
    df_total = df_data.groupby(grouping_cols)[cols.udise_col].count().reset_index()

    # Merge the total to the summary data
    df_summary = df_total.merge(data_pivot, on=grouping_cols, how='left')

    # Rename the columns to make them more readable
    df_summary.rename(columns={
        cols.udise_col : cols.tot_schools,
        cols.scheme_inprogress_upper_case : cols.scheme_in_progress,
        cols.schemes_total_students_small_case : cols.schemes_total_students}, inplace=True)

    return df_summary


def pre_process_BRC_merge(raw_data:pd.DataFrame):
    """
    Function to process the students receiving notebooks raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw common pool data

    Returns:
    -------
    DataFrame object of common pool data processed and ready for mapping with BRC-CRC data
    """

    print('Pre Processing before BRC merge called in students receiving notebooks')

    # Replace the null values in issued students column with zero
    raw_data[cols.schemes_issued_students] = raw_data[cols.schemes_issued_students].replace('Null', 0)

    # Group the data to school level
    df_grouped = raw_data.groupby(initial_group_levels, sort=False).agg(
        {cols.schemes_total_students_small_case : 'sum', cols.schemes_issued_students : 'sum'}).reset_index()

    # Set the status column based on total students vs issued students
    status_conditions = [
        (df_grouped[cols.schemes_issued_students] >= df_grouped[cols.schemes_total_students_small_case]),
        ((df_grouped[cols.schemes_total_students_small_case] > df_grouped[cols.schemes_issued_students]) & (df_grouped[cols.schemes_issued_students] != 0)),
        (df_grouped[cols.schemes_issued_students] == 0)

    ]
    status_values = [cols.scheme_completed, cols.scheme_in_progress, cols.scheme_not_started]
    df_grouped['status'] = np.select(status_conditions, status_values)

    return df_grouped

def get_unranked_elem_report(df_data:pd.DataFrame, grouping_cols:list, agg_dict:dict):
    """
    Custom function to generate the elementary report until unranked level

    Parameters:
    -----------
    ceo_rpt_raw_data: Pandas DataFrame 
        DataFrame object of the processed raw data
    grouping_cols: list
        The list of columns to group by
    agg_dict: dict
        The columns to aggregate and their corresponding functions
    
    Returns:
    --------
    Pandas DataFrame object of the unranked secondary level report
    """
    # Filter the data to elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Get notebooks issue status wise summary at grouping level
    df_data = _get_notebooks_issue_status_summary(df_data, grouping_cols)

    return df_data


def get_unranked_sec_report(df_data:pd.DataFrame, grouping_cols:list, agg_dict:dict):
    """
    Custom function to generate the secondary report until unranked level

    Parameters:
    -----------
    ceo_rpt_raw_data: Pandas DataFrame 
        DataFrame object of the processed raw data
    grouping_cols: list
        The list of columns to group by
    agg_dict: dict
        The columns to aggregate and their corresponding functions
    
    Returns:
    --------
    Pandas DataFrame object of the unranked secondary level report
    """
    # Filter the data to secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]

    # Get notebooks issue status wise summary at grouping level
    df_data = _get_notebooks_issue_status_summary(df_data, grouping_cols)

    return df_data