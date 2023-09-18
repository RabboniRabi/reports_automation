import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import utilities.dbutilities as dbutilities
credentials_dict = dbutilities.read_conn_credentials('db_credentials_rabboni.json')
query="""select
	sscc.district_name,
	sscc.block_name,
	sscc.udise_code,
	sscc.school_name,
	usd.u_id,
	usd.teacher_name,
	tt.type_teacher,
	usa.AnswerString
from
	udise_staffreg usd
join teacher_type tt

on
	tt.id = usd.teacher_type
join students_school_child_count sscc

on
	usd.udise_code = sscc.udise_code
join user_selected_answers usa

on
	usa.userId = usd.u_id
where
	usa.qset_id in ({0},{1},{2})"""

values=[30246,30248,30247]
df1= dbutilities.fetch_data_as_df_V2(credentials_dict,query,values)
df.to_excel(r'C:\Users\TAMILL\Data Reporting\reports\extracted\Aug_23\TPD_quizes3.xlsx',sheet_name='detials')
