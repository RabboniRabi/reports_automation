"""
Script to extract student transition data class-wise in one go
"""
import utilities.file_utilities as file_utilities
import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
def data_extraction():
    """
    Function to extract student transition data
    Returns:

    """
    class_studying_id = {
        "Grade_1-2_stu_trans_count": [1, 2],
        "Grade_2-3_stu_trans_count": [2, 3],
        "Grade_3-4_stu_trans_count": [3, 4],
        "Grade_4-5_stu_trans_count": [4, 5],
        "Grade_5-6_stu_trans_count": [5, 6],
        "Grade_6-7_stu_trans_count": [6, 7],
        "Grade_7-8_stu_trans_count": [7, 8],
        "Grade_8-9_stu_trans_count": [8, 9],
        "Grade_9-10_stu_trans_count": [9, 10],
        "Grade_10-11_stu_trans_count": [10, 11],
        "Grade_11-12_stu_trans_count": [11, 12],
    }
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
    dir_path = file_utilities.get_gen_reports_dir_path()
    trans_df = pd.DataFrame()
    grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name]
    for grade, grade_list in class_studying_id.items():
        print(grade)
        df_trans_count = dbutilities.fetch_data_as_df(credentials_dict, 'student_transition_sch_lvl_info.sql',
                                          params=[grade, grade_list[0], grade_list[1]])
        print(df_trans_count)
        df_grade_count = dbutilities.fetch_data_as_df(credentials_dict, 'student_class_sch_lvl_info.sql', params= [str(grade_list[0])+ '_count', grade_list[0]])
        print(df_grade_count)
        merge_df = df_trans_count.merge(df_grade_count, how='left', on=grouping_levels)

        trans_df = pd.concat([trans_df, merge_df], axis=1)
        print(trans_df)
    file_utilities.save_to_excel({'Report': trans_df}, "students_transtition_v1.xlsx", dir_path=dir_path)

if __name__ == "__main__":
    data_extraction()


