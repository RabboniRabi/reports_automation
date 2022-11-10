"""

Module with functions to:
- Update records of total schools count for each day the script is run on.
- Collate and track UDISE codes for each day the script is run on.

"""
import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities

import pandas as pd
import os
from datetime import date
from pathlib import Path


def day_wise_tracking(master_file_name, df_today):
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

    """"

   if (~os.path.exists(master_file_path)):
        # create file
        print('')
        # Save all the data
    else:
        # Read the file
        # update UDISE present/absent
        print('')
        
    """


    if os.path.exists(r'C:\Users\Admin\Downloads\data_trends.xlsx'):
        df_master = pd.read_excel(r'C:\Users\Admin\Downloads\data_trends.xlsx')
        df_tobeconcat = df_today[~df_master.isin(df_today)].dropna()
        df_tobeconcat[date.today()] = 'TRUE'
        df_master = pd.concat([df_master, df_tobeconcat], axis=0).fillna("FALSE")
        df_master[date.today()] = df_master['UDISE'].isin(df_today['UDISE'])
    else:
        df_day1 = pd.read_excel(r'C:\Users\Admin\Downloads\Test for Daily.xlsx', sheet_name='Sheet1')
        df_formaster = df_day1.groupby(['District', 'UDISE'])['UDISE'].count()
        df_formaster = pd.ExcelWriter(r'C:\Users\Admin\Downloads\data_trends.xlsx')
        df_formaster.to_excel(df_day1, index = False)
        df_formaster.save()





def main():
    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_school_child_count_summary.sql')


    # Alternatively
    # Ask the user to select the School enrollment abstract excel file.
    school_enrollment_abstract = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(school_enrollment_abstract, sheet_name='Report', skiprows=0)


    # district wise count of schools based on UDISE code - Separate function for this

    # UDISE day wise tracking (present/absent) - Separate function for this
    df_today = pd.read_excel(r'C:\Users\Admin\Downloads\Test for Daily.xlsx', sheet_name='Sheet2')
    day_wise_tracking('data_trends.xlsx', df_today)





if __name__ == "__main__":
    main()