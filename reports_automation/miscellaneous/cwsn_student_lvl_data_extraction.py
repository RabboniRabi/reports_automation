"""
Script to extract cwsn student level data between two academic years, who didn't transition in the previous academic year.
"""
import sys
sys.path.append('../')
import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities
import data_cleaning.column_cleaner as column_cleaner
import utilities.report_splitter_utilities as report_splitter

def get_student_level_data():
    """
    Function to extract cwsn student level data between current academic year's and previous year
    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
    dir_path = file_utilities.get_gen_reports_dir_path()

    # Get the CWSN students previous year information from the database as a Pandas DataFrame object
    cwsn_df_prev_yr = dbutilities.fetch_data_as_df(credentials_dict, 'CWSN_students_information_2022-23.sql')
    cwsn_df_prev_yr = column_cleaner.standardise_column_names(cwsn_df_prev_yr)
    pd.set_option('display.max_colwidth', None)
    print(cwsn_df_prev_yr[cols.stu_emis_no])
    file_utilities.save_to_excel({'Report': cwsn_df_prev_yr}, "cwsn_students_2022_23.xlsx", dir_path=dir_path)

    # Get the students current academic year information from the database as a Pandas DataFrame object
    stu_df_curr_yr = dbutilities.fetch_data_as_df(credentials_dict, 'students_information_2023-24.sql')
    stu_df_curr_yr = column_cleaner.standardise_column_names(stu_df_curr_yr)
    stu_df_curr_yr = stu_df_curr_yr.astype({
        cols.stu_emis_no: "string"
        })

    file_utilities.save_to_excel({'Report': cwsn_df_prev_yr}, "students_info_2023-24.xlsx", dir_path=dir_path)

    # To find out whether the previous academic year cwsn students emis id are there in the current academic year student data
    cwsn_df_prev_yr['Emis_Id'] = cwsn_df_prev_yr[cols.stu_emis_no].apply(utilities.xlookup, args=(stu_df_curr_yr[cols.stu_emis_no], "Yes", False))


    file_utilities.save_to_excel({'Report': cwsn_df_prev_yr}, "cwsn_students.xlsx", dir_path=dir_path)

if __name__ == "__main__":
    report_splitter.split_report_given_file("cwsn_students_not_transitioned.xlsx", "cwsn_student_not_transitioned", "cwsn_stu_details_not_transitioned", cols.district_name)
