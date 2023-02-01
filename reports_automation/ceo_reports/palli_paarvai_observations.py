"""

Module with functions to:
    -Will report the % of observations conducted vs the target no.of observations to be conducted by the CEOs and DEOs
"""
import sys
sys.path.append('../')

import utilities.column_names_utilities as cols

from datetime import datetime
import utilities.column_names_utilities as cols


import pandas as pd
from datetime import date


# Define elementary indexes for pivoting
elem_pivot_index = [cols.district_name, cols.deo_name_elm, cols.school_level, cols.school_category]
# Define secondary indexes for pivoting
sec_pivot_index = [cols.district_name, cols.deo_name_sec, cols.school_level, cols.school_category]



def _process_data_for_report(df_data, pivot_index, ceo_target_val, deo_target_val):
    """
    Internal function to get a report ready data by:
        - Pivoting and getting mapped statuses count of schools at grouping level
        - Total count of schools at grouping level
    
    Parameters:
    ----------
    df_data: Pandas DataFrame
        DataFrame object of the data to be processed for report
    pivot_index: list
        The list of values to pivot by
    ceo_target_val: str
        The value of the CEO target
    deo_target_val: str
        The value of the DEO target
    """
    df_data_pivot = pd.pivot_table(df_data, index=pivot_index, columns=cols.pp_designation, values=cols.udise_col,\
        aggfunc='count').reset_index().fillna(0)

    # Targets are kept as 12 for both the designations
    # Merging both target and raw data
    df_data_pivot[cols.deo_target] = deo_target_val
    df_data_pivot[cols.perc_DEO_obs] = df_data_pivot['DEO']/df_data_pivot[cols.deo_target]
    df_data_pivot[cols.ceo_target] = ceo_target_val
    df_data_pivot[cols.perc_DEO_obs] = df_data_pivot['CEO']/df_data_pivot[cols.ceo_target]

    return df_data_pivot

def pre_process_BRC_merge(raw_data:pd.DataFrame):
    """
    Function to process the Palli Parvai raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw Palli Parvai data

    Returns:
    -------
    DataFrame object of Palli Parvai data processed and ready for mapping with BRC-CRC data
    """

    print('Pre Processing before BRC merge called in Palli Parvai')

    # Raw data only for the specific month - previous month
    raw_data[cols.observation_date] = raw_data[cols.observation_date].dt.month
    raw_data = raw_data[raw_data[cols.observation_date] == (datetime.now().month - 1)]
    
    # Filter the data to only the ceo and deo observations
    raw_data = raw_data[raw_data[cols.observed_by].str.contains('|'.join(['ceo','deo']))]
    # Filter data by removing entries with null designations
    raw_data = raw_data[~(raw_data[cols.designation] == 'Null')]

    return raw_data


def post_process_BRC_merge(raw_data_brc_merged:pd.DataFrame):
    """
    Function to process the Palli Parvai raw data after being merged with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data_brc_merged: Pandas DataFrame
        The raw Palli Parvai data merged with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of Palli Parvai data ready for report generation
    """

    print('post process called for Palli Parvai report')

    # Replace null values with 0s
    raw_data_brc_merged.replace('Null', value=0, inplace=True)
    # Filter out data whose school level values are 0
    raw_data_brc_merged = raw_data_brc_merged[~raw_data_brc_merged[cols.school_level].isin([0])]

    return raw_data_brc_merged


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

    # Prepare the data for elementary report
    df_data = _process_data_for_report(df_data, elem_pivot_index, ceo_target_val=3, deo_target_val=6)

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

    # Prepare the data for secondary report
    df_data = _process_data_for_report(df_data, sec_pivot_index, ceo_target_val=3, deo_target_val=6)

    return df_data
