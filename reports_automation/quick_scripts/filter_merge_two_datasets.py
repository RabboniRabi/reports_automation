"""
Script to merge subset of values in two dataframes
"""
import sys
sys.path.append('../')

import pandas as pd
import utilities.utilities as utilities

enrollment_file_path = '/home/rabboni/Downloads/Sch-Enrollment-Abstract.xlsx'
PET_file_path = '/home/rabboni/Downloads/PET.xlsx'

df_enrol_report = pd.read_excel(enrollment_file_path, sheet_name='Report', skiprows=0)

# Filter only government and non primary schools from enrolment data
df_enrol_govt = utilities.filter_dataframe_column(df_enrol_report, 'Management_Type', ['Government'])
df_enrol_govt_non_prim = utilities.filter_dataframe_column(df_enrol_govt, 'Category_Group'\
            , ['Middle School', 'High School', 'Higher Secondary School'])



df_pet_report = pd.read_excel(PET_file_path, sheet_name='PET', skiprows=0)

# Filter only government and non primary schools from PET data
df_pet_govt = utilities.filter_dataframe_column(df_pet_report, 'Management_Type', ['Government'])
df_pet_govt_non_prim = utilities.filter_dataframe_column(df_pet_govt, 'Category_Group'\
            , ['Middle School', 'High School', 'Higher Secondary School'])

# Merge the school data with PET teachers
df_merged = pd.merge(df_enrol_govt_non_prim, df_pet_govt_non_prim, how='outer', \
                on=['District', 'Block', 'UDISE_Code', 'School_Name'])

# Test that it has been merged properly
df_merged.to_excel('/home/rabboni/Documents/EMIS/Data Reporting/reports/extracted/Aug_23/PET_schools_dets.xlsx', sheet_name='PET_schools_dets')