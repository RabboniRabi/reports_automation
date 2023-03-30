"""
Module with custom functions to create students ageing in common pool report.
"""

import sys
sys.path.append('../')

import pandas as pd
import functools as ft
import utilities.column_names_utilities as cols



# Define elementary indexes for pivoting
elem_pivot_index = [cols.deo_name_elm, cols.block_name]
# Define secondary indexes for pivoting
sec_pivot_index = [cols.deo_name_sec, cols.block_name]

# Define elementary report classes
elem_classes = [1,2,3,4,5,6,7,8]

# Define secondary report classes
sec_classes = [1,2,3,4,5,6,7,8,9,10,11]


def _get_classwise_common_pool_data(df_data, pivot_index, classes):
    """
    Internal function to get the classwise common pool data by calculating:
     -  ageing (time spent in common pool)
     - classwise total
     - cwsn students in common pool
    
    Parameters:
    ----------
    df_data: Pandas DataFrame
        The common pool data to work on
    pivot_index: list
        The list of index values to pivot on
    classes: list
        The list of classes that will be in the data post pivot - Will vary for elementary and secondary


    Returns:
    -------
    Pandas DataFrame object of classwise common pool data
    """
    # Get school category wise ageing count in each class
    data_pivot_ageing = pd.pivot_table(df_data, values=cols.students_ageing30_count, \
                        index=pivot_index ,columns=[cols.class_number], aggfunc='sum',fill_value=0).reset_index()

    # Update with the total ageing data
    data_pivot_ageing[cols.ageing] = data_pivot_ageing[classes].sum(axis=1)

    # Get the school category wise total of students in common pool
    data_pivot_total = pd.pivot_table(df_data, values=cols.total_cp_students, index=pivot_index,
                          aggfunc='sum').reset_index()

    # Get the school category wise total of CWSN students in common pool
    data_pivot_cwsn = pd.pivot_table(df_data, values=cols.total_cwsn_students, index=pivot_index,
                           aggfunc='sum').reset_index()     

    # Define the dataframes to merge
    data_frames_merge = [data_pivot_ageing, data_pivot_total, data_pivot_cwsn]

    data_final = ft.reduce(lambda left, right: pd.merge(left, right, how='left',on=pivot_index), data_frames_merge)

    # Convert all header value types to string
    data_final.columns = data_final.columns.map(str)

    return data_final


def pre_process_BRC_merge(raw_data:pd.DataFrame):
    """
    Function to process the common pool raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw common pool data

    Returns:
    -------
    DataFrame object of common pool data processed and ready for mapping with BRC-CRC data
    """

    print('Pre Processing before BRC merge called in common pool')

    # Drop the educational district colum as it will not be needed
    raw_data.drop(columns=cols.edu_district_name, axis=1, inplace=True)
    # Remove  un-aided and central government schools from report
    raw_data = raw_data[~raw_data[cols.school_type].isin([cols.un_aided,cols.central_govt])]

    return raw_data

def post_process_BRC_merge(raw_data_brc_merged:pd.DataFrame):
    """
    Function to process the common pool raw data after being merged with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data_brc_merged: Pandas DataFrame
        The raw common pool data merged with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of common pool data ready for report generation
    """

    print('post process called for common pool report')

    # Clean the data by replacing null values with 0
    raw_data_brc_merged.replace('Null', value=0, inplace=True)

    # Define desired data type of a sub set of columns
    convert_dtype_columns = {
        cols.students_ageing30_count: 'int', 
        cols.total_cp_students: 'int', 
        cols.total_cwsn_students: 'int',
        cols.class_number:'int'}
    # Convert the data type of above defined columns
    raw_data_brc_merged = raw_data_brc_merged.fillna(0).astype(convert_dtype_columns)

    # Clean the data by removing rows whose column values for school type is 0
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

    # Get classwise common pool data
    df_data = _get_classwise_common_pool_data(df_data, elem_pivot_index, elem_classes)

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
    df_data = _get_classwise_common_pool_data(df_data, sec_pivot_index, sec_classes)

    return df_data