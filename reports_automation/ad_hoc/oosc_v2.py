"""
Module to generate the OoSC report for reason type to be admitted breakdown.
"""
import sys
sys.path.append("../")

import pandas as pd
import numpy as np
import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities

# Get the reason type column
reason_type_col = cols.reason_type
def reason_type_breakdown(df,grouping_levels):
    """
    Function to group for school level data, filtering the reason type
    Args:
        df:
        grouping_levels:

    Returns:

    """
    # Clean the reason type values
    df[reason_type_col].replace(to_replace=['To be admitted', 'To be Admitted '], value=cols.to_be_admitted,
                                inplace=True)
    # Filter the data to reason type matching 'to be admitted' status
    df_to_be_admitted = df[df[cols.reason_type] == cols.to_be_admitted]

    # Get the student admitted/not admitted summary of the filtered to be admitted data
    df_status_to_be_admitted = pd.pivot_table(df_to_be_admitted, values=cols.emis_number,
                                                 index=grouping_levels, columns=[cols.oosc_student_status],
                                                 aggfunc='count', fill_value=0).reset_index()
    # Renaming the admitted and not admitted column name
    df_status_to_be_admitted.rename(columns={'Not Admitted': 'To Be Admitted Not Admitted',
                                             'Admitted': 'To Be Admitted Admitted'}, inplace=True)

    # Filter the data to reason type matching 'non-target' status
    df_non_target = df[df[cols.reason_type] == cols.non_target]

    # Get the student admitted/not admitted summary of the filtered non target data
    df_status_non_target = pd.pivot_table(df_non_target, values=cols.emis_number, index=grouping_levels,
                                          columns=[cols.oosc_student_status], aggfunc='count', fill_value=0).reset_index()

    # Renaming the admitted and not admitted column name
    df_status_non_target.rename(columns={'Not Admitted': 'Non Target Not Admitted',
                                         'Admitted': 'Non Target Admitted'}, inplace=True)

    # Filter the data to reason type matching 'to be verified' status
    df_to_be_verified = df[df[cols.reason_type] == cols.to_be_verified]

    # Get the student admitted/not admitted summary of the filtered to be verified data
    df_status_to_be_verified = pd.pivot_table(df_to_be_verified, values=cols.emis_number, index=grouping_levels,
                                              columns=[cols.oosc_student_status], aggfunc='count', fill_value=0).reset_index()
    # Renaming the admitted and not admitted column name
    df_status_to_be_verified.rename(columns={'Not Admitted': 'To Be Verified Not Admitted',
                                             'Admitted': 'To Be Verified Admitted'}, inplace=True)
    # Merging the to be admitted and non target data into a single dataframe
    df_pivot = df_status_to_be_admitted.merge(df_status_non_target, on=grouping_levels, how='left')

    # Merging the to be verified in the main dataframe
    df_pivot.merge(df_status_to_be_verified, on=grouping_levels, how='left')

    return df_pivot


def main():
    # Ask the user to select the excel file to clean the columns.
    report = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(report, sheet_name='Report', skiprows=4)
    # Define the levels to group the data by
    grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name]
    reason_type_breakdown(df_report, grouping_levels)

if __name__ == "__main__":
    main()
