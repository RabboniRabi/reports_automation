"""
Module with functions to do custom processing of source data
 - Change the class section wise schemes completed status to school level completed statuses.
"""

import sys
sys.path.append('../')

import pandas as pd
import numpy as np

import utilities.column_names_utilities as cols

# Group the data to school level
initial_group_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.cate_type]

def process_base_report(raw_data:pd.DataFrame):
    """
    Function to process the schemes raw class section wise data to school level completed statuses

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw schemes data

    Returns:
    -------
    DataFrame object of schemes data at school level
    """

    print('Processing base report for Schemes')

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
    status_values = [cols.scheme_comp, cols.scheme_inprogress, cols.scheme_nt_strt]
    df_grouped['status'] = np.select(status_conditions, status_values)

    return df_grouped


def data_summary(df_base_report, summary_sheet_args):
    """
    Function to create custom summary of data for given summary sheet arguments

    Parameters:
    -----------
    df_base_report: Pandas DataFrame
        The base data from which the custom data summary is to be extracted
    summary_sheet_args: dict
        Dictionary of arguments required to the data summary
    """

    # Get the grouping levels
    grouping_levels = summary_sheet_args['grouping_levels']
    # Get issue status wise count of schools at grouping level
    data_pivot = pd.pivot_table(df_base_report, values=cols.udise_col, index=grouping_levels, \
                    columns=[cols.scheme_status], aggfunc='count',fill_value=0).reset_index()

    # Get the total number of schools
    df_total = df_base_report.groupby(grouping_levels)[cols.udise_col].count().reset_index()

    # Merge the total to the summary data
    df_summary = df_total.merge(data_pivot, on=grouping_levels, how='left')

    return df_summary