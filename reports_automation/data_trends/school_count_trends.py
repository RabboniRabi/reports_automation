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
import utilities.column_names_utilities as cols

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
        Name of the master file with schools count data
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

    # Rename the UDISE column with date + count string
    df_today_grouped.rename(columns={udise_col: utilities.get_today_date()}, inplace=True)

    if(os.path.exists(master_file_path)):
        # If the file exists, update and save the data with today's count
        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)

        # Merge the data for the day with the master data
        df_master = df_master.merge(df_today_grouped)

    else:
        # If file doesnt exist, create data and save for day 1
        df_master = df_today_grouped
    return df_master



def day_wise_tracking(master_file_name, sheet_name, df_today, dist_col, udise_col):
    """
    Function to track the presence/absence of UDISE codes on the day the script is run.
    The function also updates the master tracking excel file with any new UDISE codes found.

    Parameters:
    -----------
    master_file_name: str
        Name of the master file with the day wise tracking of UDISE code
    sheet_name: str
        Name of the sheet with the data
    df_today: DataFrame
        Data of school UDISE codes fetched today
    dist_col: str
        The name of the column in the sheet with District names
    udise_col: str
        The name of the column in the sheet with UDISE values 
    Returns:
    -------
    DataFrame Object of UDISE sheet data updated with the days' UDISE code tracking

    """

    # Get the full file path to the master trends tracking file - assuming in generated reports folder
    master_file_path = os.path.join(file_utilities.get_gen_reports_dir_path(), master_file_name)
    # Get today's date
    today_date = utilities.get_today_date()

    # Update df_today to be the subset of district and UDISE columns
    df_today = df_today[[dist_col, udise_col,cols.block_name,cols.school_name,cols.category_type,cols.management_type]]

    # If file does not exist
    if not os.path.exists(master_file_path):
        # The master data will be today's data as there is no previous data
        df_master = df_today.copy()
        # Create a new column to mark the presence of all UDISes fetched today as TRUE
        df_master[today_date] = 'True'

    else:
        # Read the master data
        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)
        
        # Get a True/False series of all UDISES that are present in currently fetched data but not in master (True)
        udise_present_today_not_in_master = ~df_today[cols.udise_col].isin(df_master[cols.udise_col])

        df_new_UDISEs = df_today[udise_present_today_not_in_master].dropna()


        # Create a column in df_new_UDISEs marking all new UDISEs present today as TRUE
        df_new_UDISEs[today_date] = 'True'

        # Concatenate the new UDISES found for today with the master data, filling FALSE for previous days
        df_master = pd.concat([df_master, df_new_UDISEs], axis=0).fillna('False')

        # The concatenation of new UDISEs to the master data will mark the presence of rest of UDISES as FALSE
        # in the new column (with today's date)
        # This is updated by checking those UDISEs present both in master and today and marking them as TRUE
        df_master[today_date] = df_master[udise_col].isin(df_today[udise_col])

    # Sort the data
    df_master.sort_values(by=[dist_col, udise_col], ascending=[True, True], inplace=True)
    return df_master


def student_count_tracking(master_file_name, sheet_name, df_today, dist_col, udise_col,student_count_col):
    """
    Function to track the count of students on the day the script is run.
    The function also updates the master tracking excel file with any new UDISE codes found.

    Parameters:
    -----------
    master_file_name: str
        Name of the master file with the day wise tracking of UDISE code
    sheet_name: str
        Name of the sheet with the data
    df_today: DataFrame
        Data of school UDISE codes fetched today
    dist_col: str
        The name of the column in the sheet with District names
    udise_col: str
        The name of the column in the sheet with UDISE values
    student_count_col: int
        The count of students in that particular school on the day the script is run.

    Returns:
    --------
    DataFrame Object of student counts in each UDISE on the day script is run

    """

    # Get the full file path to the master trends tracking file - assuming in generated reports folder
    master_file_path = os.path.join(file_utilities.get_gen_reports_dir_path(), master_file_name)
    # Get today's date
    today_date = utilities.get_today_date()

    # Update df_today to be the subset of district, UDISE, total students columns
    df_today = df_today[[dist_col, udise_col,cols.block_name,cols.school_name,cols.category_type,cols.management_type,student_count_col]]

    # If file does not exist
    if not os.path.exists(master_file_path):
        # Create a new column to mark the presence of all UDISes fetched today as TRUE
        df_master = df_today.copy().groupby([dist_col,udise_col])[[student_count_col]].sum().reset_index()

        df_master.rename(columns={student_count_col: today_date},inplace=True)

        df_master['No. of days data changes'] = '0'
    else:
        # Read the master data
        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)

        # Get a True/False series of all UDISES that are present in currently fetched data but not in master (True)
        df_today = df_today.groupby([dist_col,udise_col])[[student_count_col]].sum().reset_index()

        # Concatenate the new UDISES found for today with the master data, filling FALSE for previous days
        df_master = df_master.merge(df_today).fillna(0)

    # Rename the column with today's date
    df_master.rename(columns={student_count_col: today_date}, inplace=True)
    # Sort the data
    df_master.sort_values(by=[dist_col, udise_col], ascending=[True, True], inplace=True)

    df_master['No. of days data changes'] = df_master.drop(columns=[cols.district_name, cols.udise_col,
                                                                    cols.block_name,cols.school_name,cols.category_type,cols.management_type,
                                                                    'No. of days data changes']).nunique(axis=1)
    df_master['No. of days data changes'] = df_master['No. of days data changes'] - 1

    df_master.insert(6,'No. of days data changes',df_master.pop('No. of days data changes'))

    return df_master

def teacher_count_tracking(master_file_name, sheet_name, df_today, dist_col, udise_col,teacher_count_col):
    """
    Function to track the count of students on the day the script is run.
    The function also updates the master tracking excel file with any new UDISE codes found.

    Parameters:
    -----------
    master_file_name: str
        Name of the master file with the day wise tracking of UDISE code
    sheet_name: str
        Name of the sheet with the data
    df_today: DataFrame
        Data of school UDISE codes fetched today
    dist_col: str
        The name of the column in the sheet with District names
    udise_col: str
        The name of the column in the sheet with UDISE values
    teacher_count_col: int
        The count of teachers in that particular school on the day the script is run.

    Returns:
    --------
    DataFrame Object of teacher counts in each UDISE on the day script is run

    """

    # Get the full file path to the master trends tracking file - assuming in generated reports folder
    master_file_path = os.path.join(file_utilities.get_gen_reports_dir_path(), master_file_name)
    # Get today's date
    today_date = utilities.get_today_date()

    # Update df_today to be the subset of district, UDISE, total students columns
    df_today = df_today[[dist_col, udise_col,cols.block_name,cols.school_name,cols.category_type,cols.management_type,teacher_count_col]]

    # If file does not exist
    if not os.path.exists(master_file_path):
        # Create a new column to mark the presence of all UDISes fetched today as TRUE
        df_master = df_today.copy().groupby([dist_col,udise_col])[[teacher_count_col]].sum().reset_index()

        df_master.rename(columns={teacher_count_col: today_date + ' count'},inplace=True)

        df_master['No. of days data changes'] = '0'
    else:
        # Read the master data
        df_master = pd.read_excel(master_file_path, sheet_name=sheet_name)

        # Get a True/False series of all UDISES that are present in currently fetched data but not in master (True)

        df_today = df_today.groupby([dist_col,udise_col])[[teacher_count_col]].sum().reset_index()

        # Concatenate the new UDISES found for today with the master data, filling FALSE for previous days
        df_master = df_master.merge(df_today).fillna(0)

    # Rename the column with today's date
    df_master.rename(columns={teacher_count_col: today_date}, inplace=True)
    # Sort the data
    df_master.sort_values(by=[dist_col, udise_col], ascending=[True, True], inplace=True)

    df_master['No. of days data changes'] = df_master.drop(columns=[cols.district_name, cols.udise_col,
                                                                    cols.block_name,cols.school_name,cols.category_type,cols.management_type,
                                                                    'No. of days data changes']).nunique(axis=1)
    df_master['No. of days data changes'] = df_master['No. of days data changes'] - 1

    df_master.insert(6,'No. of days data changes',df_master.pop('No. of days data changes'))

    return df_master


def main():
    
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_school_child_count.sql')


    # Alternatively
    # Ask the user to select the School enrollment abstract excel file.
    #school_enrollment_abstract = file_utilities.user_sel_excel_filename()
    #df_report = pd.read_excel(school_enrollment_abstract, sheet_name='Report',skiprows=4)
    #print(df_report.columns)


    # Get a data frame updated with the latest school count
    df_school_count = day_wise_school_count_tracking('school_count_trends.xlsx', 'school_count_tracking', df_report,cols.district_name, cols.udise_col)

    # Get a data frame updated with latest UDISE tracking (present/absent)
    df_daywise_tracking = day_wise_tracking('school_count_trends.xlsx', 'daywise_UDISE_tracking', df_report, cols.district_name, cols.udise_col)
    df_student_count =student_count_tracking('stu_teach_count_trends.xlsx', 'student_count_tracking', df_report, cols.district_name, cols.udise_col, 'Total_Students')

    df_teacher_count =teacher_count_tracking('stu_teach_count_trends.xlsx', 'teacher_count_tracking', df_report, cols.district_name, cols.udise_col, 'Teaching_Staff')
    # Save the updated master data
    df_sheet_dict_school = {
        'school_count_tracking': df_school_count,
        'daywise_UDISE_tracking': df_daywise_tracking
        }
    df_sheet_dict_st_teach = {'student_count_tracking':df_student_count,
        'teacher_count_tracking': df_teacher_count}

    file_utilities.save_to_excel(df_sheet_dict_school, 'school_count_trends.xlsx')
    file_utilities.save_to_excel(df_sheet_dict_st_teach, 'stu_teach_count_trends.xlsx')



if __name__ == "__main__":
    main()