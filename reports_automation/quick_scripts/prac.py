import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import utilities.dbutilities as dbutilities
credentials_dict = dbutilities.read_conn_credentials('db_credentials_rabboni.json')
values=[30243,30247]
df1= dbutilities.fetch_data_as_df(credentials_dict,"TPD_teacher_detials_with_answers.sql",values)
df1.to_excel(r'C:\Users\TAMILL\Data Reporting\reports\extracted\Aug_23\TPD_quizes6.xlsx',sheet_name='detials')
