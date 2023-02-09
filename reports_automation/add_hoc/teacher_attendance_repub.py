
import sys
sys.path.append('../')

import pandas as pd
import utilities.file_utilities as file_utilities

data1 = pd.read_excel(r'C:\Users\Admin\Downloads\EE Attendance.xlsx',sheet_name='data')
data2 = pd.read_excel(r'C:\Users\Admin\Downloads\EE Attendance.xlsx',sheet_name='final')

data3 = pd.pivot_table(data1,columns='training_date',aggfunc='count', index='Attended_Teacher_ID').reset_index()

print(data3)

file_utilities.save_to_excel({'teacher_training_att': data3}, 'teacher_att_split.xlsx',\
         dir_path = file_utilities.get_gen_reports_dir_path())
