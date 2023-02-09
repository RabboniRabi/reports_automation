"""
Module to generate the OoSC report with focus on % to be admitted
"""
import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities

import utilities.column_names_utilities as cols
import pandas as pd
import numpy as np

# Get the reason type column
reason_type_col = cols.reason_type


def _get_reason_type_summary(df, grouping_level):
    """
    Internal function to get the reason type-grouping level wise summary
    of OSC data.

    Parameters:
    -----------
    df: DataFrame
        The raw OSC data
    grouping_level: list
        The list of levels to group the data by
    """

    # Clean the reason type values
    df[reason_type_col].replace(to_replace=['To be admitted', 'To be Admitted '] , value=cols.to_be_admitted, inplace=True)

    # Get reason type wise summary of OSC data
    df_pivot = pd.pivot_table(df, values=cols.student_name, \
                        index=grouping_level ,columns=[reason_type_col], aggfunc='count',fill_value=0).reset_index()

    return df_pivot


def run():
    """
    Main function that calls other internal functions to generate the report
    """

    file_path = file_utilities.get_curr_month_source_data_dir_path() + '/OSC-Survey-Full-Rpt.xlsx'
    df_report = pd.read_excel(file_path, sheet_name='Report',skiprows=4)

    # Define the levels to group the data by
    grouping_levels = [cols.district_name]

    # Summarise the data to grouping levels and reasons types
    df_reason_type_sum = _get_reason_type_summary(df_report, grouping_levels)

    # Get the common pool to be surveyed data
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the common pool to be surveyed details from the database as a Pandas DataFrame object
    common_pool_to_be_surveyed = dbutilities.fetch_data_as_df(credentials_dict, 'common_pool_to_be_surveyed.sql')

    # Group to district and count number of students
    common_pool_to_be_surveyed_grouped = common_pool_to_be_surveyed.groupby(cols.district_name)[cols.school_name].count().reset_index()
    common_pool_to_be_surveyed_grouped.rename(columns={cols.school_name: cols.to_be_surveyed}, inplace=True)

    # Merge the data
    df_oosc = df_reason_type_sum.merge(common_pool_to_be_surveyed_grouped, on=cols.district_name)

    # Calculate the grouping wise % to be admitted 
    df_oosc[cols.perc_to_be_admitted] = df_oosc[cols.to_be_admitted]/ df_oosc[cols.to_be_surveyed]

    # sort the data by % to be admitted
    df_oosc.sort_values(cols.perc_to_be_admitted, ascending=False, inplace=True)

    file_utilities.save_to_excel({'Report':df_oosc}, 'OoSC_Report.xlsx')

if __name__ == "__main__":
    run()