"""
Module with custom functions to create sports battery test students report.
"""

import sys
sys.path.append('../')

import pandas as pd

import utilities.column_names_utilities as cols

def _get_book_issue_status_summary(df_data, grouping_cols):
    """
    Internal function to get summary of schools' book issue statuses at grouping level

    Parameters:
    ----------
    df_data: Pandas DataFrame
        The sports battery tests data to work on
    grouping_cols: list
        The list of columns to group by

    Returns:
    --------
    The summary of schools' book issue statuses at grouping level
    """

    # Get issue status wise count of schools at grouping level
    data_pivot = pd.pivot_table(df_data, values=cols.udise_col, \
                        index=grouping_cols,columns=[cols.scheme_status], aggfunc='count',fill_value=0).reset_index()


    # Get the total number of schools
    df_total = df_data.groupby(grouping_cols)[cols.udise_col].count().reset_index()

    # Merge the total to the summary data
    df_summary = df_total.merge(data_pivot, on=grouping_cols)

    # Rename the columns to make them more readable
    df_summary.rename(columns={
        cols.scheme_inprogress :  cols.scheme_in_progress,
        cols.scheme_comp: cols.scheme_completed,
        cols.scheme_nt_strt : cols.scheme_not_started,
        cols.udise_col : cols.tot_schools}, inplace=True)

    return df_summary

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

    # Get book issue status wise summary at grouping level
    df_data = _get_book_issue_status_summary(df_data, grouping_cols)

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

    # Get book issue status wise summary at grouping level
    df_data = _get_book_issue_status_summary(df_data, grouping_cols)

    return df_data