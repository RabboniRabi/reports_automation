from datetime import datetime
from datetime import timedelta

import sys
sys.path.append('../')

import utilities.dbutilities as dbutilities
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import pandas as pd

#Dictionary for groupby criteria
grouping_levels = [cols.district_name]
grouping_agg_dict = {cols.udise_col : 'count'}


def _process_data(df_tchrs_attendance, df_schools):
    """
    Internal function to process the data to generate the report
    
    Parameters:
    -----------
    df_tchrs_attendance: Pandas DataFrame
        The teachers' attendance data as a Pandas DataFrame object
    df_schools: Pandas DataFrame
        The schools count data
    Returns:
    -------
    The data processed as a report.
    """

    # Drop the unneccesary rows
    df_tchrs_attendance = df_tchrs_attendance.drop(columns=['c','edate'])

    # Group and aggregate the data
    df_grouped = df_tchrs_attendance.groupby(grouping_levels).agg(grouping_agg_dict).reset_index()

    # Merging the data with the total schools count from the SQL query above (from df_report)
    df_grouped = pd.merge(df_grouped, df_schools, on=[cols.district_name])  

    # Renaming columns to report appropriate names
    df_grouped.rename(columns = {
        cols.district_name : cols.district,
        cols.distinct_udise_count : cols.tot_schools, 
        cols.udise_col : cols.unmarked_schools}, inplace=True)

    # Calculate percentage of unmarked schools over the last 7 days
    df_grouped[cols.perc_7_days_unmarked_schls] = df_grouped[cols.unmarked_schools] / df_grouped[cols.tot_schools]

    # Sort the data based on highest number of schools unmarked in a district
    df_grouped.sort_values([cols.perc_7_days_unmarked_schls], ascending=False, inplace=True)

    # Add the grand total row to the processed data
    cols_agg_dict = {
        cols.tot_schools : 'sum',
        cols.unmarked_schools : 'sum',
        cols.perc_7_days_unmarked_schls : 'mean'
        }

    df_grouped.loc[-1,:] = df_grouped.aggregate(cols_agg_dict)

    df_grouped.at[-1, cols.district] = "Grand Total"

    # Changing the format from float to percentage
    df_grouped.loc[:, cols.perc_7_days_unmarked_schls] = df_grouped[cols.perc_7_days_unmarked_schls].map('{:.2%}'.format)

    return df_grouped


def _format_save_report(df_report, df_tchrs_attendance):
    """
    Internal function to format the report and save

    Parameters:
    ----------
    df_report: Pandas DataFrame
        The report to be formatted
    """
    # Drop the unneccesary rows
    df_tchrs_attendance = df_tchrs_attendance.drop(columns=['c','edate'])

    #Adding borders and formatting to both the dataframes
    df_report = df_report.style.set_properties(**{'text-align': 'center','border-color':'black','border-width':'0.1em'})
    df_tchrs_attendance = df_tchrs_attendance.style.set_properties(**{'text-align': 'center','border-color':'black','border-width':'0.1em'})

    # Saving the data to an excel sheet both the unmarked Schools and the abstracted file
    df_sheet_dict = {'Unmarked Schools Abstract': df_report, 'Unmarked Schools Detailed': df_tchrs_attendance}
    file_utilities.save_to_excel(df_sheet_dict, 'Teacher Attendance-Unmarked Schools Report.xlsx', \
            dir_path=file_utilities.get_curr_day_month_gen_reports_dir_path(), engine='xlsxwriter')

    #Additional Formatting

    # Open the file in OpenPyXl to apply some formatting using OpenPyXl
    file_path = file_utilities.get_file_path('Teacher Attendance-Unmarked Schools Report.xlsx', file_utilities.get_curr_day_month_gen_reports_dir_path())
    df_final = openpyxl.load_workbook(file_path)
    main_page = df_final['Unmarked Schools Abstract']
    main_page.insert_rows(idx=0,amount=1)

    # First Row - Heading with the date from and date to and also formatting the same.
    day1 = (datetime.today() - timedelta(days=7)).strftime('%d/%m/%Y')
    day2 = (datetime.today() - timedelta(days=1)).strftime('%d/%m/%Y')
    main_page['A1'].value = '% of Teachers not marking Student Attendance from {} to {}'.format(day1,day2)
    font1 = Font(size=12, bold=True)
    main_page['A1'].font = font1
    main_page.merge_cells('A1:D1')
    alignment = Alignment(horizontal='center',vertical='center')
    main_page['A1'].alignment = alignment
    bd = Side(border_style='thin',color='00000000')
    border = Border(top=bd,left=bd,right=bd,bottom=bd)

    # Final Save
    df_final.save(file_path)

def run():
    """
    Main function that calls other functions to generate the report
    """

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials_attendance.json')

    # Get the latest Schools unmarked details from the SQL query file
    df_tchrs_attendance = dbutilities.fetch_data_as_df(credentials_dict, 'teacher_unmarked_weekly.sql')

    # Get the total schools abstract from the SQL query file
    df_schools = dbutilities.fetch_data_as_df(credentials_dict, 'total_schools.sql')

    # Process the data and get the report
    df_report = _process_data(df_tchrs_attendance, df_schools)

    # Format the report and save
    _format_save_report(df_report, df_tchrs_attendance)


if __name__ == "__main__":
    run()










