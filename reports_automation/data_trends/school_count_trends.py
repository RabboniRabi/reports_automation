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

    file_utilities.save_to_excel({sheet_name: df_master}, master_file_name)    




def day_wise_tracking(master_file_name, df_today,columns_tb_copied,sheet_name):
    """
    Function to track the presence/absence of UDISE code on the day the script is run.
    The function also updates the master tracking excel file with any new UDISE codes found.

    Parameters:
    -----------
    master_file_name: str
        Name of the master file with the day wise tracking of UDISE code
    df_today: DataFrame
        Data of school UDISE codes fetched today

    Returns
    -------

    """
    # check if master udise tracking exists??

    master_file_path = os.path.join(fileutilities.get_gen_reports_dir_path(), master_file_name)
    if ~os.path.exists(master_file_path):
        df_master = df_today[columns_tb_copied].copy()
        df_master[date.today()] = 'True'
        file_utilities.save_to_excel({sheet_name: df_master}, master_file_name)

    else:
        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)
        df_tobeconcat = df_today[~df_master.isin(df_today)].dropna()
        df_tobeconcat[date.today()] = 'TRUE'
        df_master = pd.concat([df_master, df_tobeconcat], axis=0).fillna("FALSE")
        df_master[date.today()] = df_master['UDISE'].isin(df_today['UDISE'])
        file_utilities.save_to_excel({sheet_name: df_master}, master_file_name)

def main():
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_school_child_count_summary.sql')


    # Alternatively
    # Ask the user to select the School enrollment abstract excel file.
    school_enrollment_abstract = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(school_enrollment_abstract, sheet_name='Report', skiprows=4)


    # district wise count of schools based on UDISE code - Separate function for this
    day_wise_school_count_tracking(
        'school_count_trends.xlsx', 'School count tracking', df_report, ['District'], 'UDISE_Code')

    # UDISE day wise tracking (present/absent) - Separate function for this
    #df_today = pd.read_excel(r'C:\Users\Admin\Downloads\Test for Daily.xlsx', sheet_name='Sheet2')
    #day_wise_tracking('data_trends.xlsx', df_today)

    day_wise_tracking('school_count_trends.xlsx',df_report,df_today['District','UDISE'],'master_sheet')



if __name__ == "__main__":
    main()