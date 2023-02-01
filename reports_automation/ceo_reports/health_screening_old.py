"""
Module with functions to create health screening report for CEO reports.
This module contains functions to create reports for:
- Health screening students completed
- Health screening schools completed
"""

import os
import sys
sys.path.append('../')


import pandas as pd

import utilities.file_utilities as file_utilities
import utilities.format_utilities as format_utilities
import utilities.dbutilities as dbutilities
import utilities.report_utilities as report_utilities
import utilities.column_names_utilities as cols

merge_dict = {
    'on_values' : [cols.district_name, cols.block_name, cols.school_name, cols.school_category, cols.udise_col],
    'how' : 'left'
}

# Define the grouping levels for elementary report
elem_rep_group_level = [cols.district_name, cols.block_name, cols.beo_user, cols.beo_name, \
cols.deo_name_elm, cols.school_category, cols.school_level]

# Define the grouping levels for secondary report
scnd_rep_group_level = [cols.district_name, cols.block_name, cols.deo_name_sec, \
cols.school_category, cols.school_level]

# Build the arguments dictionary to do ranking for the students health report
students_ranking_args_dict = {
    'agg_dict': {cols.screened: 'sum', cols.total: 'sum'},
    'ranking_val_desc': cols.perc_screened,
    'num_col': cols.screened,
    'den_col': cols.total,
    'sort': True,
    'ascending': False
}

# Build the arguments dictionary to do ranking for the schools health report
schools_ranking_args_dict = {
    'agg_dict': {cols.total: 'count', cols.fully_comp: 'sum'},
    'ranking_val_desc': cols.perc_comp,
    'num_col': cols.fully_comp,
    'den_col': cols.total,
    'sort': True,
    'ascending': False
}


def _get_data_with_brc_mapping():
    """
    Function to fetch the health data merged with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of health data updated with BRc-CRC mapping
    """
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'health_screening_status.sql')

    # Save the fetched data for reference
    #file_utilities.save_to_excel({'Report': df_report}, 'health_screening_status.xlsx', dir_path = file_utilities.get_source_data_dir_path())

    # Use the fetched data for testing, instead of reading from db
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'health_screening_status.xlsx')
    df_report = pd.read_excel(file_path)

    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(df_report, merge_dict)

    return data_with_brc_mapping


def _get_students_health_report(df_data, group_levels, agg_cols, school_level):
    """
    Internal function to create the health report based on student count with the data
    grouped at given grouping levels and for given shool level.

    Parameters:
    ----------
    df_data: Pandas DataFrame
        The health data updated with BRC mapping. 
    group_levels: list
        The list of columns to group by
    agg_cols: list
        The list of columns to aggregate by      
    school_level: str
        The school level. Typically: 'Elementary' or 'Secondary'

    Returns:
    --------
    DataFrame object of student count based health report        
    """

    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([school_level])]    

    data_grouped = df_data.groupby(group_levels, as_index=False)[agg_cols].agg('sum')

    # Calculate and add a column of percentage students screened data
    data_grouped[cols.perc_screened] = data_grouped[cols.screened] / data_grouped[cols.total]

    # Sort the data
    data_grouped.sort_values(by=[cols.perc_screened], ascending=False, inplace=True)

    return data_grouped

def _get_data_with_school_level_scrn_status(df):
    """
    Internal function to update the data with school level
    Fully completed, Partially Completed, 'Not Started' screening statuses.

    Parameters:
    -----------
    df: Pandas DataFrame
        The health data to be updated with screening statuses of schools

    Returns:
    -------
    DataFrame object of data updated with schools screening statuses
    """
    # Compute whether a school has completed screening, partially completed or not started
    series_completed = (df[cols.total] - df[cols.screened] <= 0 ) & (df[cols.total]  != 0)
    series_not_started =  df[cols.screened] == 0
    series_partially_completed =  ~(series_completed | series_not_started)
    school_col_index = df.columns.get_loc(cols.school_name)            
    # Insert the computed values as series into the dataframe next to the school column
    df.insert(school_col_index+1,cols.fully_comp, series_completed)
    df.insert(school_col_index+2,cols.part_comp, series_partially_completed)
    df.insert(school_col_index+3,cols.not_started, series_not_started)


    return df

def get_students_elementary_health_report(df_data = None):
    """
    Function to create the health report of elementary level students at BEO level

    Parameters:
    -----------
    df_data: Pandas DataFrame
        The health data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of elementary students' health report
    """
    
    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    #data_grouped = df_data.groupby(elem_rep_group_level, as_index=False)[cols.screened, cols.total].agg('sum')

    # Replace the line below with the line above when restoring beo level ranking
    data_grouped = df_data.groupby([cols.district_name, cols.deo_name_elm, cols.school_category], as_index=False)[cols.screened, cols.total].agg('sum')

    #elem_report = _get_students_health_report(df_data, elem_rep_group_level, [cols.screened, cols.total], cols.elem_schl_lvl)

    # Replace the line below with the line above when restoring beo level ranking
    #elem_report = _get_students_health_report(df_data, [cols.district_name, cols.deo_name_elm, cols.school_category], [cols.screened, cols.total], cols.elem_schl_lvl)

    elem_report = report_utilities.get_elem_ranked_report(\
        data_grouped, 'percent_ranking', students_ranking_args_dict, 'HC_Stud', 'Health')

    return elem_report



def get_students_secondary_health_report(df_data = None):
    """
    Function to create the health report of secondary level students at DEO level

    Parameters:
    -----------
    df_data: Pandas DataFrame
        The health data updated with BRC mapping. (Default is None)
    
    Returns:
    -------
    DataFrame object of secondary students' health report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Filter the data to Secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]    

    #data_grouped = df_data.groupby(scnd_rep_group_level, as_index=False)[cols.screened, cols.total].agg('sum')

    # Replace the line below with the line above when restoring beo level ranking
    data_grouped = df_data.groupby([cols.district_name, cols.deo_name_sec, cols.school_category], as_index=False)[cols.screened, cols.total].agg('sum')


    #scnd_report = _get_students_health_report(df_data, scnd_rep_group_level, [cols.screened, cols.total], cols.scnd_schl_lvl)

    # Replace the line below with the line above when restoring beo level ranking
    #scnd_report = _get_students_health_report(df_data, [cols.district_name, cols.deo_name_sec, cols.school_category], [cols.screened, cols.total], cols.scnd_schl_lvl)

    # Get the Secondary report
    scnd_report = report_utilities.get_sec_ranked_report(\
        data_grouped, 'percent_ranking', students_ranking_args_dict, 'HC_Stud', 'Health')

    return scnd_report



def get_schools_elementary_health_report(df_data = None):
    """
    Function to fetch the health report of elementary level schools at BEO level

    Parameters:
    -----------
    df_data: Pandas DataFrame
        The health data updated with BRC mapping. (Default is None)

    Returns:
    -------
    DataFrame object of elementary students' health report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()
    
    # Update the data with schools' screening status
    df_data = _get_data_with_school_level_scrn_status(df_data)

    # Filter the data to Elementary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Group the data for elementary  reports generation
    #data_for_elem = df_data.groupby(elem_rep_group_level, as_index=False)[cols.total, cols.fully_comp].agg('sum')

    # Replace the line below with the line above when restoring BEO level ranking
    data_for_elem = df_data.groupby([cols.district_name, cols.deo_name_elm, cols.school_category, cols.school_level], as_index=False).agg({
        cols.total: 'count',
        cols.fully_comp: 'sum'
    })

    # Get the Elementary report
    elem_report = report_utilities.get_elem_ranked_report(\
        data_for_elem, 'percent_ranking', schools_ranking_args_dict, 'HC_Sch', 'Health')

    return elem_report


def get_schools_secondary_health_report(df_data = None):
    """
    Function to fetch the health report of secondary level students at DEO level

    Parameters:
    -----------
    df_data: Pandas DataFrame
        The health data updated with BRC mapping. (Default is None)
    
    Returns:
    -------
    DataFrame object of secondary students' health report
    """

    # If no data was passed, fetch it
    if (df_data is None):
        # Get the BRC-CRC mapped health data
        df_data = _get_data_with_brc_mapping()

    # Update the data with schools' screening status
    df_data = _get_data_with_school_level_scrn_status(df_data)

    # Filter the data to Secondary school type
    df_data = df_data[df_data[cols.school_level].isin([cols.scnd_schl_lvl])]
    
    # Group the data for secondary reports generation
    """data_for_secnd = df_data.groupby(scnd_rep_group_level, as_index=False).agg({
        cols.total: 'count',
        cols.fully_comp: 'sum'
    })"""

    # Replace the line below with the line above
    data_for_secnd = df_data.groupby([cols.district_name, cols.deo_name_sec, cols.school_category], as_index=False).agg({
        cols.total: 'count',
        cols.fully_comp: 'sum'
    })
    
    # Get the Secondary report
    secnd_report = report_utilities.get_sec_ranked_report(\
        data_for_secnd, 'percent_ranking', schools_ranking_args_dict, 'HC_Sch', 'Health')

    return secnd_report

def run():
    """
    Function to call other internal functions and create the Health screening status reports
    """
    # Get the health data updated with BRC mapping
    data_with_brc_mapping = _get_data_with_brc_mapping()

    students_elem_report = get_students_elementary_health_report(data_with_brc_mapping.copy())

    students_scnd_report = get_students_secondary_health_report(data_with_brc_mapping.copy())

    schools_elem_report = get_schools_elementary_health_report(data_with_brc_mapping.copy())

    schools_scnd_report = get_schools_secondary_health_report(data_with_brc_mapping.copy())

    # Define the levels and columns to subtotal
    level_subtotal_cols_dict = {1:cols.deo_name_elm, 2:cols.school_category}
    # Define the columns to aggregate and their respective aggregate function
    agg_cols_func_dict = {cols.total:'sum', cols.perc_screened:'mean'}

    # Save the elementary students health screening report
    format_utilities.format_col_to_percent_and_save(students_elem_report, cols.perc_screened, 'Health Screening Report',
            'Health Screening Elementary Students Report.xlsx',
            dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())

    # Save the elementary schools health screening report
    format_utilities.format_col_to_percent_and_save(schools_elem_report, cols.perc_comp, 'Health Screening Report',
            'Health Screening Elementary Schools Report.xlsx',
            dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())
   
    # Save the secondary students health screening report
    format_utilities.format_col_to_percent_and_save(students_scnd_report, cols.perc_screened, 'Health Screening Report',
            'Health Screening Secondary Students Report.xlsx',
            dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())
   
    # Save the secondary schools health screening report
    format_utilities.format_col_to_percent_and_save(schools_scnd_report, cols.perc_comp, 'Health Screening Report',
            'Health Screening Secondary Schools Report.xlsx',
            dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())  




if __name__ == "__main__":
    run()
