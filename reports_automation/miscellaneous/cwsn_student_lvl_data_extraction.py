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
class_transitioned_id = {
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
    10: 11,
    11: 12
}


def get_student_level_data():
    """
    Function to extract cwsn student level data between current academic year's and previous year
    Returns:

    """

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
    dir_path = file_utilities.get_gen_reports_dir_path()
    not_transitioned_df = pd.DataFrame()
    for prev_class_id, curr_class_id in class_transitioned_id.items():
        print("prev: ", prev_class_id)
        print("curr", curr_class_id)
        # Get the CWSN students previous year information from the database as a Pandas DataFrame object
        df = dbutilities.fetch_data_as_df(credentials_dict, 'CWSN_students_information_2022-23.sql', params=[prev_class_id, prev_class_id])
        not_transitioned_df = pd.concat([not_transitioned_df, df])
    not_transitioned_df = column_cleaner.standardise_column_names(not_transitioned_df)
    not_transitioned_df = not_transitioned_df.astype({
        cols.stu_emis_no: 'string'
    })
    file_utilities.save_to_excel({'Report': not_transitioned_df}, "cwsn_students_retained_v1.xlsx", dir_path=dir_path)
    split_df = report_splitter.split_report(not_transitioned_df, cols.district_name)
    report_splitter.save_split_report(split_df, "cwsn_student_retained_v1" )



if __name__ == "__main__":
    report_splitter.split_report_given_file("cwsn_students_not_transitioned_v1.xlsx", "Detailed", "cwsn_stu_details_not_transitioned", cols.district_name)
    #get_student_level_data()
