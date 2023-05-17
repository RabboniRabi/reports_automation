"""
Module with custom functions to create sports equipment delivery status report.
"""

import sys
sys.path.append('../')

import pandas as pd

import utilities.column_names_utilities as cols


def _get_delivery_status_summary(df_data, grouping_cols):
    """
    Internal function to get summary of delivery statuses at grouping level

    Parameters:
    ----------
    df_data: Pandas DataFrame
        The sports delivery status data to work on
    grouping_cols: list
        The list of columns to group by

    Returns:
    --------
    The summary of schools' book issue statuses at grouping level
    """

    # Get issue status wise count of schools at grouping level
    data_pivot = pd.pivot_table(df_data, values=cols.udise_col, \
                        index=grouping_cols,columns=[cols.delivery_status], aggfunc='count',fill_value=0).reset_index()


    # Get the total number of schools
    df_total = df_data.groupby(grouping_cols)[cols.udise_col].count().reset_index()

    # Merge the total to the summary data
    df_summary = df_total.merge(data_pivot, on=grouping_cols, how='left')

    # Rename the columns to make them more readable
    df_summary.rename(columns={
        cols.not_deliverd :  cols.not_delivered,
        cols.udise_col : cols.tot_schools
        }, inplace=True)

    # Swap the order of not delivered and partially delivered columns
    not_delivered_col_index = df_summary.columns.get_loc(cols.not_delivered)
    part_delivered_col_index = df_summary.columns.get_loc(cols.part_delivered)
    df_summary_columns = df_summary.columns.to_list()
    df_summary_columns[part_delivered_col_index], df_summary_columns[not_delivered_col_index] = \
        df_summary_columns[not_delivered_col_index], df_summary_columns[part_delivered_col_index] 

    df_summary = df_summary.reindex(columns=df_summary_columns)

    """# Rearranging the columns for better reading order
    list_of_cols = """

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
    df_data = _get_delivery_status_summary(df_data, grouping_cols)

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
    df_data = _get_delivery_status_summary(df_data, grouping_cols)

    return df_data