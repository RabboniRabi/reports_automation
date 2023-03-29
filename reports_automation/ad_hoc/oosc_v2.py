"""
Module to generate the OoSC report for reason type to be admitted breakdown.
"""
import sys
sys.path.append("../")

import pandas as pd
import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities

# Get the reason type column
reason_type_col = cols.reason_type
def reason_type_breakdown(df,grouping_levels):
    """
    Function to group for school level data, filtering the reason type with respect to
    student status - student admitted and not admitted.

    Parameters:
    -----------
        df: Pandas Dataframe
            OoSC data
        grouping_levels: list
            The list of levels to group the data by.

    Returns:
    -----------
    Dataframe object of the final filtering the reason type with its count.
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
    # Renaming the student admitted and not admitted column name
    df_status_to_be_admitted.rename(columns={cols.not_admttd: cols.admitted_not_admitted,
                                             cols.stdnt_admttd: cols.admitted}, inplace=True)

    # Filter the data to reason type matching 'non-target' status
    df_non_target = df[df[cols.reason_type] == cols.non_target]

    # Get the student admitted/not admitted summary of the filtered non target data
    df_status_non_target = pd.pivot_table(df_non_target, values=cols.emis_number, index=grouping_levels,
                                          columns=[cols.oosc_student_status], aggfunc='count', fill_value=0).reset_index()

    # Renaming the student admitted and not admitted column name
    df_status_non_target.rename(columns={cols.not_admttd: cols.non_target_not_admitted ,
                                         cols.stdnt_admttd: cols.non_target_admitted}, inplace=True)

    # Filter the data to reason type matching 'to be verified' status
    df_to_be_verified = df[df[cols.reason_type] == cols.to_be_verified]

    # Get the student admitted/not admitted summary of the filtered to be verified data
    df_status_to_be_verified = pd.pivot_table(df_to_be_verified, values=cols.emis_number, index=grouping_levels,
                                              columns=[cols.oosc_student_status], aggfunc='count', fill_value=0).reset_index()
    # Renaming the student admitted and not admitted column name
    df_status_to_be_verified.rename(columns={cols.not_admttd: cols.verified_not_admitted,
                                             cols.stdnt_admttd: cols.verified_admitted}, inplace=True)

    # Merging the to be admitted and non target data into a single dataframe
    df_pivot = df_status_to_be_admitted.merge(df_status_non_target, on=grouping_levels, how='left')
    # Merging the above merge and to be verified in the main dataframe
    df_final = df_pivot.merge(df_status_to_be_verified, on=grouping_levels, how='left')

    # Replacing the null values with zeo
    df_final.fillna(0, inplace=True)

    return df_final


def main():
    """
    Main function that calls other internal functions to generate the report


    """
    # Ask the user to select the excel file to clean the columns.
    report = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(report, sheet_name='Report', skiprows=4)
    # Define the levels to group the data by
    grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.category_type]
    df = reason_type_breakdown(df_report, grouping_levels)

    # Saving in the current month generated folder
    report_save_path = file_utilities.get_curr_day_month_gen_reports_dir_path() + '/oosc_report.xlsx'
    file_utilities.save_to_excel({'Report': df}, report_save_path)


if __name__ == "__main__":
    main()
