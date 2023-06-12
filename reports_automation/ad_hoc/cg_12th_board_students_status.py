"""
Career Guidance 12th Board Examination Students Status Report


"""







import sys
from datetime import datetime
sys.path.append('../')
import pandas as pd
import os
import numpy as np
import utilities.file_utilities as file_utilities
import utilities.utilities as utilities

# Columns that will be used for the GroupBy:
group_levels = ['District',	'Block', 'UDISE', 'SchoolName', 'School_Category', 'management']

# Getting the file path for the source data:
file_path = os.path.join(file_utilities.get_curr_month_source_data_dir_path(),
                         'Naan-Mudhalvan-CG-HM-Survey-Rpt_9thJune230pm.xlsx')

# Reading the excel
df_data = pd.read_excel(file_path, 'Student Wise', skiprows=4)
#df_data = df_raw_data.groupby(group_levels, as_index=False).agg(
    #Total_Students=('EMIS_No', 'count'))

# Creating the conditions required for each column

Total_Pass = [(df_data['Exam_Result_Status'] == 'pass')]

Total_Fail = [(df_data['Exam_Result_Status'] == 'fail')]

Total_Applied = [(df_data['Exam_Result_Status'] == 'pass') & (df_data['student_applied'] == 'Yes')]

Total_Applied_with_clgnm = [(df_data['Exam_Result_Status'] == 'pass') & (df_data['student_applied'] == 'Yes') &
                            (df_data['college_name'].notna())]

Total_Applied_without_clgnm = [(df_data['Exam_Result_Status'] == 'pass') &
                               (df_data['student_applied'] == 'Yes') & (df_data['college_name'].isna())]

Total_Applied_without_clgnm_doubtful = [(df_data['Exam_Result_Status'] == 'pass') &
                               (df_data['student_applied'] == 'Yes') & (df_data['college_name'].isna()) &
                                            (df_data['student_certificate'].str.contains('10th|11th'))]

Total_Not_Applied = [(df_data['Exam_Result_Status'] == 'pass') & (df_data['student_applied'] == 'No')]

Total_Not_Updated = [(df_data['Exam_Result_Status'] == 'pass') & (df_data['student_applied'] == 'Not updated')]

choices = [1]
df_data['Total_Students'] = 1
df_data['Total_Pass'] = np.select(Total_Pass, choices, default=0)
df_data['Total_Fail'] = np.select(Total_Fail, choices, default=0)
df_data['Total_Applied'] = np.select(Total_Applied, choices, default=0)
df_data['Total_Applied_with_clgnm'] = np.select(Total_Applied_with_clgnm, choices, default=0)
df_data['Total_Applied_without_clgnm'] = np.select(Total_Applied_without_clgnm, choices, default=0)
df_data['Total_Applied_without_clgnm_doubtful'] = np.select(Total_Applied_without_clgnm_doubtful, choices, default=0)
df_data['Total_Applied_without_clgnm_other_reasons'] = df_data['Total_Applied_without_clgnm'] - \
                                                       df_data['Total_Applied_without_clgnm_doubtful']
df_data['Total_Not_Applied'] = np.select(Total_Not_Applied, choices, default=0)
df_data['Total_Not_Updated'] = np.select(Total_Not_Updated, choices, default=0)

df_student_level = df_data.drop(columns=['Exam_Result_Status', 'student_applied',
                            'Reason', 'reason_others',	'entrance_exam', 'student_certificate', 'Loan_Available',
                            'college_id', 'college_name', 'education_category', 'institution_type'], inplace=True)

df_school_level = df_data.groupby(group_levels, as_index=False)['Total_Students', 'Total_Pass', 'Total_Fail',
    'Total_Applied', 'Total_Applied_with_clgnm', 'Total_Applied_without_clgnm',
        'Total_Applied_without_clgnm_doubtful', 'Total_Applied_without_clgnm_other_reasons',
                                    'Total_Not_Applied', 'Total_Not_Updated'].sum()


file_utilities.save_to_excel({'cg_student_status': df_school_level},
                             utilities.get_date_appended_excel_filename('cg_12th_board_student_status'))
