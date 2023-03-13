"""
Module with custom functions to create sports battery test students report.
"""

import sys
sys.path.append('../')

import pandas as pd

import utilities.column_names_utilities as cols

def _get_perc_event_completion_summary(df_data, grouping_cols, agg_dict):
    """
    Internal function to get summary of % students completing events in the battery tests

    Parameters:
    ----------
    df_data: Pandas DataFrame
        The sports battery tests data to work on
    grouping_cols: list
        The list of columns to group by
    agg_dict: dict
        The columns to aggregate and their corresponding functions

    Returns:
    --------
    The sports battery test data grouped and updated with percent students completing events
    """
    # Group the data
    df_grouped = df_data.groupby(grouping_cols).agg(agg_dict).reset_index()

    # Add % battery tests completion data
    df_grouped[cols.perc_50m_comp] = df_grouped[cols.m50_comp_stu]/df_grouped[cols.sports_tot_stu]
    df_grouped[cols.perc_600m_800m_comp] = df_grouped[cols.m600_800_comp_stu]/df_grouped[cols.sports_tot_stu]
    df_grouped[cols.perc_6_10m_shutt_comp] = df_grouped[cols.shuttle_comp_stu]/df_grouped[cols.sports_tot_stu]
    df_grouped[cols.perc_4kg_shot_comp] = df_grouped[cols.kg4_shot_comp_stu]/df_grouped[cols.sports_tot_stu]
    df_grouped[cols.perc_long_jump_comp] = df_grouped[cols.long_jump_comp_stu]/df_grouped[cols.sports_tot_stu]

    # Drop the battery test completion numbers as percent values will be used for report
    df_grouped.drop(columns=[cols.m50_comp_stu, cols.m600_800_comp_stu, cols.shuttle_comp_stu, \
                cols.kg4_shot_comp_stu, cols.long_jump_comp_stu], inplace=True)

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

    # Get event wise percentage completion status at grouping level
    df_data = _get_perc_event_completion_summary(df_data, grouping_cols, agg_dict)

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

    # Get event wise percentage completion status at grouping level
    df_data = _get_perc_event_completion_summary(df_data, grouping_cols, agg_dict)

    return df_data