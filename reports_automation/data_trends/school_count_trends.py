"""

Module with functions to:
- Update records of total schools count for each day the script is run on.
- Collate and track UDISE codes for each day the script is run on.

"""
import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities

import pandas as pd
import os
from datetime import date
from pathlib import Path

def day_wise_school_count_tracking(master_file_name, sheet_name, df_today, group_levels, udise_col):
    """
    Function to track the number of schools at given grouping levels on the day the script is run.
    The day's count is updated in the master tracking excel file.

    Parameters:
    -----------
    master_file_name: str
        Name of the master file with the day wise count of schools
    sheet_name: str
        The name of the sheet with the day wise count of schools    
    df_today: DataFrame
        Data of school UDISE codes fetched today
    group_levels: str
        The columns in the data to group by (Eg: district/educational district/block)
    udise_col: str
        The name of the column in the sheet with UDISE values 
    """

    # Get the full file path to the master trends tracking file - assuming in generated reports folder
    master_file_path = os.path.join(file_utilities.get_gen_reports_dir_path(), master_file_name)

    # Group the data fetched for today by grouping level, counting the number of UDISE codes
    df_today_grouped = df_today.groupby(group_levels)[udise_col].count().reset_index()


    # Calculate and insert grand total of UDISE codes for the day
    df_today_grouped.loc['Grand Total'] = ['Grand Total', df_today_grouped[udise_col].sum()]


    # Rename the UDISE column with counts
    df_today_grouped.rename(columns={udise_col: utilities.get_today_date() + ' count'}, inplace=True)

    
    if(os.path.exists(master_file_path)):
        # If the file exists, update and save the data with today's count

        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)

        # Merge the data for the day with the master data
        df_master = df_master.merge(df_today_grouped)
    
    else:
        # If file doesnt exist, create data and save for day 1
        df_master = df_today_grouped
    return df_master



def day_wise_tracking(master_file_name, sheet_name,df_today,columns_tb_copied,udise_col):
    """
    Function to track the presence/absence of UDISE code on the day the script is run.
    The function also updates the master tracking excel file with any new UDISE codes found.

    Parameters:
    -----------
    master_file_name: str
        Name of the master file with the day wise tracking of UDISE code
    df_today: DataFrame
        Data of school UDISE codes fetched today
    sheet_name: Name of the sheet with the data
    new_udises: The list of UDISE codes that appear in today's report but wasn't available in the earlier days
    columns_tb_copied: The list of udises today
    Returns
    -------

    """
    # check if master sheet exists, if it doesn't, create the master sheet for day 1, else add to the master sheet.

    master_file_path = os.path.join(file_utilities.get_gen_reports_dir_path(), master_file_name)

    # Update df_today to be the subset of given columns
    df_today = df_today[columns_tb_copied]
    if not os.path.exists(master_file_path):
        print('file does not exist')
        df_master = df_today.copy()
        df_master[date.today()] = 'True'

    else:
        print('file exists')
        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)
        new_udises = df_today[~df_master[udise_col].isin(df_today[udise_col])].dropna()
        new_udises[date.today()] = 'TRUE'
        print('new_udises: ' , new_udises)
        df_master = pd.concat([df_master, new_udises], axis=0).fillna("FALSE")

        print('df_master post concat: ', df_master)
        file_utilities.save_to_excel({'test' : df_master}, 'test.xlsx')
        # create a new column with today's date where UDISEs present both in master and today are marked true and those absent, false
        df_master[date.today()] = df_master[udise_col].isin(df_today[udise_col])

    # Rename the UDISE column with counts
    df_master.rename(columns={date.today(): utilities.get_today_date() + ' present'}, inplace=True)
    df_master.sort_values(['District'], ascending=[True]).reset_index()
    return df_master


def main():
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_school_child_count.sql')

    print('df_report fetched from db: ', df_report)


    # Alternatively
    # Ask the user to select the School enrollment abstract excel file.
    #school_enrollment_abstract = file_utilities.user_sel_excel_filename()
    #df_report = pd.read_excel(school_enrollment_abstract, sheet_name='Report')


    # district wise count of schools based on UDISE code - Separate function for this
    df_school_count = day_wise_school_count_tracking('school_count_trends.xlsx', 'school_count_tracking', df_report,['District'],'UDISE_Code')

    # UDISE day wise tracking (present/absent) - Separate function for this
    #df_today = pd.read_excel(r'C:\Users\Admin\Downloads\Test for Daily.xlsx', sheet_name='Sheet2')
    #day_wise_tracking('data_trends.xlsx', df_today)
    #df_today = pd.read_excel(r'C:\Users\Admin\Downloads\Sch-Enrollment-Abstract (9).xlsx', sheet_name='Report')

    df_daywise_tracking = day_wise_tracking('school_count_trends.xlsx','daywise_UDISE_tracking',df_report,['District','UDISE_Code'], 'UDISE_Code')

    df_sheet_dict = {
        'school_count_tracking': df_school_count,
        'daywise_UDISE_tracking': df_daywise_tracking
        }
    file_utilities.save_to_excel(df_sheet_dict, 'school_count_trends.xlsx')


if __name__ == "__main__":
    main()