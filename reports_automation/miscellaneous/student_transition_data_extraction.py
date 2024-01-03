"""
Script to extract student transition data class-wise in one go
"""
import sys
sys.path.append('../')
import os
import utilities.file_utilities as file_utilities
import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import utilities.report_splitter_utilities as report_splitter_utilities
def data_extraction():
    """
    Function to extract student transition data
    Returns:

    """
    class_studying_id = {
        "'Grade_1-2_stu_trans_count'": [1, 2],
        "'Grade_2-3_stu_trans_count'": [2, 3],
        "'Grade_3-4_stu_trans_count'": [3, 4],
        "'Grade_4-5_stu_trans_count'": [4, 5],
        "'Grade_5-6_stu_trans_count'": [5, 6],
        "'Grade_6-7_stu_trans_count'": [6, 7],
        "'Grade_7-8_stu_trans_count'": [7, 8],
        "'Grade_8-9_stu_trans_count'": [8, 9],
        "'Grade_9-10_stu_trans_count'": [9, 10],
        "'Grade_10-11_stu_trans_count'": [10, 11],
        "'Grade_11-12_stu_trans_count'": [11, 12],
    }
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
    dir_path = file_utilities.get_curr_day_month_gen_report_name_dir_path("Student_transition_class-wise_details")
    grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.school_type, cols.school_category]

    for grade, grade_list in class_studying_id.items():
        df_trans_count = dbutilities.fetch_data_as_df(credentials_dict, 'student_transition_sch_lvl_info.sql',
                                          params=[grade, grade_list[0], grade_list[1]])
        df_grade_count = dbutilities.fetch_data_as_df(credentials_dict, 'student_class_sch_lvl_info.sql', params= ['class'+str(grade_list[0])+ '_count', grade_list[0]])

        merge_df = pd.merge(df_grade_count, df_trans_count, how='outer', on=grouping_levels)
        file_utilities.save_to_excel({'Report': merge_df}, grade + '.xlsx', dir_path=dir_path)



if __name__ == "__main__":
    data_extraction()


