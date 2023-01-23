"""
Module with fcustom functions to generate report at unranked level
for PET to school mapping reports
"""

import sys
sys.path.append('../')

import pandas as pd

import utilities.column_names_utilities as cols

# Define elementary indexes for pivoting
elem_pivot_index = [cols.district_name, cols.deo_name_elm, cols.school_category]
# Define secondary indexes for pivoting
scnd_pivot_index = [cols.district_name, cols.deo_name_sec, cols.school_category]



# Build the arguments dictionary to do ranking for the report
ranking_args_dict = {
    'ranking_type': 'percent_ranking',
    'agg_dict': {
        cols.fully_mapped: 'sum', 
        cols.part_mapped: 'sum',
        cols.tot_schools: 'sum'},
    'ranking_val_desc': cols.perc_fully_mapped,
    'num_col': cols.fully_mapped,
    'den_col': cols.tot_schools,
    'sort': True,
    'ascending': False
}



def _process_data_for_report(df_data, pivot_index):
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
    """
    # Pivot the table on mapping status
    df_data_pivot = pd.pivot_table(df_data, values=cols.school_name, \
                        index=pivot_index ,columns=[cols.mapping_status], aggfunc='count',fill_value=0).reset_index()

    # Update with the total schools count
    df_data_pivot[cols.tot_schools] = df_data_pivot[[cols.fully_mapped, cols.part_mapped]].sum(axis=1)

    return df_data_pivot                    



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
    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Prepare the data for elementary report
    elem_unranked_rpt = _process_data_for_report(df_data, elem_pivot_index)

    return elem_unranked_rpt 

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
    # Filter the data to Secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]

    # Prepare the data for secondary report
    sec_unranked_rpt = _process_data_for_report(df_data, scnd_pivot_index)

    return sec_unranked_rpt

