
import sys
sys.path.append('../')
from sqlalchemy import create_engine

import utilities.dbutilities as dbutilities
import utilities.file_utilities as file_utilities

readuser = 'prod2read'
readpasswd = ';\,s*c{vp8k,=3Zs'
hosturl = 'tnschools1-cluster-instance-1.cvxfty5zotmt.ap-south-1.rds.amazonaws.com'
dbname = 'tnschools_working1'


"""con_string = f'''mysql+mysqlconnector://{readuser}:{readpasswd}@{hosturl}/{dbname}'''
print('connection string: ', con_string)
cnx = create_engine(con_string).connect()
"""

credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')



# Get the latest students and teachers count
df_report = dbutilities.fetch_data_as_df(credentials_dict, 'teacher_attendance_republic.sql')

file_utilities.save_to_excel({'teacher_attendance_republic': df_report}, 'teacher_attendance_republic.xlsx',\
         dir_path = file_utilities.get_gen_reports_dir_path())

