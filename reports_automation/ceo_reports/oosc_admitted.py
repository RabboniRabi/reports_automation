"""
Module with function for custom pre-processing of OoSC admitted report
"""


import sys
sys.path.append('../')
import utilities.file_utilities as file_utilities

import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import pandas as pd

# Define the initial grouping level
initial_group_levels = [cols.block_name, cols.udise_col, cols.school_name]

def pre_process_BRC_merge(raw_data):
    """
    Function to process the CWSN raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw CWSN data

    Returns:
    -------
    DataFrame object of CWSN data processed and ready for mapping with BRC-CRC data
    """

    print('Pre Processing before BRC merge called in Oosc admitted report')

    # Rename the column names to standard format
    column_cleaner.standardise_column_names(raw_data)

    # Get the total students surveyed at the initial grouping level
    df_tot_surveyed = raw_data.groupby(initial_group_levels)[cols.emis_number].count().reset_index()


    # Rename the emis number to a more appropriate name
    df_tot_surveyed.rename(columns = {cols.emis_number: cols.oosc_tot_surveyed}, inplace = True)

    # Clean the reason type values
    raw_data[cols.reason_type].replace(to_replace=['To be admitted', 'To be Admitted '], value=cols.to_be_admitted, inplace=True)


    # Get reason type wise summary of OSC data
    df_pivot = pd.pivot_table(raw_data, values=cols.emis_number,\
                        index = initial_group_levels, columns=[cols.reason_type], aggfunc='count',fill_value=0).reset_index()


    # Filter the data to reason type matching 'to be admitted' status
    df_to_be_admitted = raw_data[raw_data[cols.reason_type] == cols.to_be_admitted]

    # Filter the data to reason type matching status other than 'to be admitted'
    df_other_reasons = raw_data[raw_data[cols.reason_type] != cols.to_be_admitted]

    # Get the student admitted/not admitted summary of the filtered to be admitted data
    df_status_pivot = pd.pivot_table(df_to_be_admitted, values=cols.emis_number,\
                        index = initial_group_levels, columns=[cols.oosc_student_status], aggfunc='count',fill_value=0).reset_index()

    # Get the student admitted/not admitted summary of the filtered other reasons data
    df_other_status_pivot = pd.pivot_table(df_other_reasons, values=cols.emis_number,\
                        index = initial_group_levels, columns=[cols.oosc_student_status], aggfunc='count',fill_value=0).reset_index()                    


    # Rename the students admitted & not admitted columns in other reasons pivot so that the 
    # column names for other reasons can be distinguished from students admitted from to be admitted
    df_other_status_pivot.rename(columns={
        cols.stdnt_admttd:cols.oosc_stu_admt_othr_reasons,
        cols.not_admttd:cols.oosc_stu_nt_admt_othr_reasons
        }, inplace=True)

    # Merge the total students surveyed, reason wise summary and student admitted summary
    df_pre_processed = df_tot_surveyed.merge(df_pivot, on=initial_group_levels, how='left')
    df_pre_processed = df_pre_processed.merge(df_status_pivot, on=initial_group_levels, how='left')
    df_pre_processed = df_pre_processed.merge(df_other_status_pivot, on=initial_group_levels, how='left')
    df_pre_processed.fillna(0, inplace=True)


    # Drop columns that will not be used for the report
    df_pre_processed.drop(columns=[cols.to_be_verified, cols.non_target], inplace=True)

    # Rename columns
    df_pre_processed.rename(columns={cols.stdnt_admttd: cols.stdnts_admttd}, inplace=True)

    return df_pre_processed
