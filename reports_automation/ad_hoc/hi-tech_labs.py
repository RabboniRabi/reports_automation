"""
Module to generate reports on uptime and usage of hi-tech labs
"""

import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import data_cleaning.column_cleaner as column_cleaner
import utilities.column_names_utilities as cols
import pandas as pd

def _get_group_levels_wise_mean_uptime(df, grouping_levels):
    """
    Internal function to get the mean uptime of hi-tech labs
    by given grouping levels

    Parameters:
    ----------
    df: Pandas DataFrame
        The hi-tech lab wise uptime data
    grouping_levels: list
        The list of levels to group by

    Returns:
    --------
    The mean uptime of hi-tech labs grouping wise
    """

    df_mean_uptime = df.groupby(grouping_levels)[cols.up_time_hrs].median().reset_index()

    df_mean_uptime[cols.up_time_hrs] = df_mean_uptime[cols.up_time_hrs].round(2)

    # sort the districts by uptime
    df_mean_uptime.sort_values(cols.up_time_hrs, ascending=False, inplace=True)

    # Rename the column uptime hours
    df_mean_uptime.rename(columns={cols.up_time_hrs: cols.mediam_up_time_hrs}, inplace=True)

    return df_mean_uptime

def run():
    """
    Main function that calls other internal functions to generate the report
    """

    file_path = file_utilities.get_curr_month_source_data_dir_path() + '/hi-tech_labs_uptime.xlsx'

    df_report = pd.read_excel(file_path, sheet_name='uptime_report',skiprows=0)
    # Rename the column names to standard format
    column_cleaner.standardise_column_names(df_report)

    df_mean_uptime = _get_group_levels_wise_mean_uptime(df_report, cols.district_name)


    report_save_path = file_utilities.get_curr_day_month_gen_reports_dir_path() + '/hi-tech_labs_report.xlsx'
    file_utilities.save_to_excel({'Report': df_mean_uptime}, report_save_path)



if __name__ == "__main__":
    run()