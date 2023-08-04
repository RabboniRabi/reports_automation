import sys
sys.path.append('../')

import pandas as pd
import utilities.column_names_utilities as cols


# Define the initial grouping level
grouping_levels = [cols.district_name, cols.block_name, cols.udise_col]


def pre_process_BRC_merge(raw_data):
    """
    Function to process the schools without enrollment raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw data

    Returns:
    -------
    DataFrame object of schools without enrollment data processed and ready for mapping with BRC-CRC data
    """
    print('Pre Processing before BRC merge called in schools without students enrollment report')

    # Filter the column total students having value 0
    df_sch_without_enrollment = raw_data[raw_data[cols.Total_Students] == 0]
    # Get the count of schools without student enrollment
    df_pivot = pd.pivot_table(df_sch_without_enrollment, values=cols.school_name, index=grouping_levels, columns=cols.Total_Students, aggfunc='count', fill_value=0).reset_index()
    df_pivot.rename(columns={
        0:cols.sch_with_no_students
    }, inplace=True)

    # Get the total number of schools
    df_total_schools = raw_data.groupby(grouping_levels).agg({cols.school_name: "count"}).reset_index()
    # Renaming the column for better readability
    df_total_schools.rename(columns={
        cols.school_name: cols.tot_schools
    }, inplace=True)
    # Merge both datasets
    df_merge = df_total_schools.merge(df_pivot, on=grouping_levels, how='left')
    df_merge.fillna(0, inplace=True)

    return df_merge
