"""
Script to get the teacher training Quiz answers from Teachers with their detials
"""
import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import utilities.dbutilities as dbutilities
credentials_dict = dbutilities.read_conn_credentials('db_credentials_rabboni.json')
connection = dbutilities.create_server_connection(credentials_dict)
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
params = [30246,30247,30248]
query = query.format(*params)
df = pd.read_sql_query(query, connection)
df.to_excel(r'C:\Users\TAMILL\Data Reporting\reports\extracted\Aug_23\TPD_quizes2.xlsx',sheet_name='detials')



