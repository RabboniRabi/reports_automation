"""
Module with custom functions to create sports battery test schools report.
"""

import sys
sys.path.append('../')

import pandas as pd

import utilities.column_names_utilities as cols

def _get_schools_completion_summary(df_data, grouping_cols):
    """
    Internal function to get summary of schools' completion of battery tests

    Parameters:
    ----------
    df_data: Pandas DataFrame
        The sports battery tests data to work on
    grouping_cols: list
        The list of columns to group by
    """

    # Get schools battery test completion summary
    df_pivot = pd.pivot_table(df_data, values=cols.udise_col, \
                        index=grouping_cols, columns=[cols.test_comp_status], aggfunc='count',fill_value=0).reset_index()

    df_total = df_data.groupby(grouping_cols)[cols.udise_col].count().reset_index()
    df_total.rename(columns={cols.udise_col:cols.tot_schools}, inplace=True)

    df_summary = df_pivot.merge(df_total, on=grouping_cols)

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

    # Get schools' completion summary of battery tests summary
    df_data = _get_schools_completion_summary(df_data, grouping_cols)

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

    # Get classwise common pool data
    df_data = _get_schools_completion_summary(df_data, grouping_cols)

    return df_data