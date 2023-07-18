"""
Script to show how many classes/sections are without class teacher
"""

import sys
sys.path.append('../')

import pandas as pd
import utilities.column_names_utilities as cols


# Define the initial grouping level
grouping_levels = [cols.district_name, cols.block_name, cols.udise_col]


def pre_process_BRC_merge(raw_data):
    """
    Function to process the sections without class teacher raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw data

    Returns:
    -------
    DataFrame object of sections without class teacher data processed and ready for mapping with BRC-CRC data
    """
    print('Pre Processing before BRC merge called in sections without class teacher report')

    # Filter the column teacher id for teachers not assigned in the classes
    df_not_assigned = raw_data[raw_data[cols.teacher_id] == cols.not_assigned]
    # Get the count of class teachers not assigned
    df_pivot = pd.pivot_table(df_not_assigned, values=cols.school_name, index=grouping_levels, columns=cols.teacher_id, aggfunc='count', fill_value=0).reset_index()
    # Renaming the column for better readability
    df_pivot.rename(columns={
        cols.not_assigned: cols.sections_without_teacher
    }, inplace=True)

    # Get the total number of sections
    df_total_sections = raw_data.groupby(grouping_levels).agg({cols.class_section: 'count'}).reset_index()
    # Renaming the column for better readability
    df_total_sections.rename(columns={
        cols.class_section: cols.tot_sections
    }, inplace=True)
    # Merge both datasets
    df_merge = df_total_sections.merge(df_pivot, on=grouping_levels, how='left')
    df_merge.fillna(0, inplace=True)

    return df_merge


