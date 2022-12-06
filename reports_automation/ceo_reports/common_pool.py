"""
Module with functions to:
- Create the common pool report for the CEO review report.
- The code will create 2 commpn pool reports
- one for elementary schools (Primary & Middle Schools) 
- another for secondary schools (High & Higher Secondary Schools)

"""

import sys
sys.path.append('../')

import utilities.utilities as utilities
import functools as ft
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.ranking_utilities as ranking_utilities
import utilities.report_utilities as report_utilities
import utilities.column_names_utilities as cols


import pandas as pd
import os
from datetime import date
from pathlib import Path


# Define elementary indexes for pivoting
elem_pivot_index = [cols.district_name, cols.deo_name_elm, cols.school_category]
# Define secondary indexes for pivoting
scnd_pivot_index = [cols.district_name, cols.deo_name_sec, cols.school_category]

# Define elementary report classes
elem_classes = [1,2,3,4,5,6,7,8,9]

# Define secondary report classes
scnd_classes = [1,2,3,4,5,6,7,8,9,10,11]

# Dictionary to define how the values to merge on and the how the merge will work.
merge_dict = {
    'on_values' : [cols. district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
}

# Build the arguments dictionary to do ranking for the report
ranking_args_dict = {
    'agg_dict': {
        cols.ageing: 'sum', 
        cols.total_cp_students: 'sum'},
    'ranking_val_desc': '% ageing in CP',
    'num_col': cols.ageing,
    'den_col': cols.total_cp_students,
    'sort': True,
    'ascending': True
}


def _get_data_with_brc_mapping():
    """
    Function to fetch the Commpon Pool data, clean and  merge with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of Common Pool data updated with BRc-CRC mapping
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_data = dbutilities.fetch_data_as_df(credentials_dict, 'common_pool_latest.sql')

    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'commonpool_classwise_report.xlsx')
    df_data = pd.read_excel(file_path, sheet_name='Abstract')

    # Drop the educational district colum as it will not be needed
    df_data.drop(columns=cols.edu_district_name, axis=1, inplace=True)
    # Remove  un-aided and central government schools from report
    df_data = df_data[~df_data[cols.school_type].isin([cols.un_aided,cols.central_govt])]

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_data, merge_dict)

    # Clean the data by replacing null values with 0
    data_with_brc_mapping.replace('Null', value=0, inplace=True)

    # Define desired data type of a sub set of columns
    convert_dtype_columns = {
        cols.students_ageing30_count: 'int', 
        cols.total_cp_students: 'int', 
        cols.total_cwsn_students: 'int',
        cols.class_number:'int'}
    # Convert the data type of above defined columns
    data_with_brc_mapping = data_with_brc_mapping.fillna(0).astype(convert_dtype_columns)

    # Clean the data by removing rows whose column values for school type is 0
    data_with_brc_mapping = data_with_brc_mapping[~data_with_brc_mapping[cols.school_level].isin([0])]

    return data_with_brc_mapping


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
    # Get chool category wise ageing count in each class
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


def get_cp_elementary_report(df_data = None):
    """
    Function to get the commpon pool elementary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The common pool data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of elementary students' CWSN report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Get classwise common pool data
    classwise_cp_data = _get_classwise_common_pool_data(df_data, elem_pivot_index, elem_classes)

    elem_report = report_utilities.get_elementary_report(classwise_cp_data, 'percent_ranking', ranking_args_dict, 'CP', 'Enrolment')

    return elem_report


def get_cp_secondary_report(df_data = None):
    """
    Function to get the commpon pool secondary level report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The school level commpon pool data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of secondary students' commpon pool report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()    

    # Filter the data to Secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]    

    # Get classwise common pool data
    classwise_cp_data = _get_classwise_common_pool_data(df_data, scnd_pivot_index, scnd_classes)

    # Get the Secondary report
    secnd_report = report_utilities.get_secondary_report(\
        classwise_cp_data, 'percent_ranking', ranking_args_dict, 'CP', 'Enrolment')

    return secnd_report
    

def run():
    """
    Function to call other internal functions and create the Common Pool reports
    """

    # Get the Commpon Pool data updated with BRC mapping
    data_with_brc_mapping = _get_data_with_brc_mapping()

    # Get the elementary report
    elem_report = get_cp_elementary_report(data_with_brc_mapping.copy())

    # Get the secondary report
    secnd_report = get_cp_secondary_report(data_with_brc_mapping.copy())

     # Save the elementary report
    file_utilities.save_to_excel({'CP Elementary Report' : elem_report}, 'CP Elementary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())   

    # Save the secondary report
    file_utilities.save_to_excel({'CP Secondary Report' : secnd_report}, 'CP Secondary Report.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())   
    
    
    

if __name__ == "__main__":
    run()
