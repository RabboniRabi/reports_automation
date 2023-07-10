"""
Module to create a report of students absent for 6 days or more.
"""

import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.column_names_utilities as cols
import pandas as pd

# Declare the class level grouping
class_level_grouping = [cols.district_name, cols.block_name, cols.udise_col, \
            cols.school_type, cols.cate_type, cols.school_name, cols.att_class_id]

def custom_base_report(df_data_set, merge_sources_configs):
    """
    Custom function to implement the logic to create the ad hoc report

    Parameters:
    ----------
    df_data_set: DataFrame
        dataset as Pandas DataFrame Objects dictionary
    merge_sources_configs: List
        List of configurations to merge the different source datasets together

    Returns:
    -------
    Base report created from source datasets and custom logic
    """

    # Get the students absent data frame object
    df_stu_abs_data = df_data_set['students_absent']

    # Filter the students who have been absent for more than 6 days
    df_stu_abs_data_filtered = utilities.filter_column_ge(df_stu_abs_data, cols.no_of_days_abs, 6)

    print('df_stu_abs_data_filtered: ', df_stu_abs_data_filtered)
    # Group to school level and count number of studnts who have been absent for more than 6 days
    df_stu_abs_grouped = df_stu_abs_data_filtered.groupby(class_level_grouping)[cols.no_of_days_abs].count().reset_index()

    print('df_stu_abs_grouped: ', df_stu_abs_grouped)

    df_stu_class_tot = df_data_set['students_classwise_total']

    # Merge students who are absent count with the students class wise total
    # Get the volunteer dataset merge configuration
    stu_class_merge_config = merge_sources_configs['students_classwise_total']
    df_merged = df_stu_abs_grouped.merge(df_stu_class_tot, how=stu_class_merge_config['merge_type'], \
                    on=stu_class_merge_config['join_on'])

    print('df_merged: ', df_merged)

    return df_merged