import sys

sys.path.append('../')
import pandas as pd
import utilities.file_utilities as file_utilities

# The dataframe with student mark details for defined management type

dir_path = file_utilities.get_curr_month_source_data_dir_path()
sslc_pvt_data_file_path = file_utilities.get_file_path('SSLC_stud_level_private_2022-23.xlsx', dir_path)
df_sslc_pvt = file_utilities.read_sheet(sslc_pvt_data_file_path, 'private_2023')
print("Data successfully read")

sslc_govt_data_file_path = file_utilities.get_file_path('SSLC_stud_level_government_2022-23.xlsx', dir_path)
df_sslc_govt = file_utilities.read_sheet(sslc_govt_data_file_path, 'govt_2023')
print("Data successfully read")

sslc_aided_data_file_path = file_utilities.get_file_path('SSLC_stud_level_aided_2022-23.xlsx', dir_path)
df_sslc_aided = file_utilities.read_sheet(sslc_aided_data_file_path, 'aided_2023')
print("Data successfully read")

# The dataframe with mother's qualification details
mother_qual_file_path = file_utilities.get_file_path('sslc_moth_qual.xlsx', dir_path)
df_mother_qual = file_utilities.read_sheet(mother_qual_file_path, 'Sheet0')


# The dataframe with mother's occupation details
moth_occ = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_moth_occ.xlsx')
print("Data successfully read")

# The dataframe with father's qualification details
fath_qual = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_fath_qual.xlsx')
print("Data successfully read")

# The dataframe with father's occupation details
fath_occ = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_fath_occ.xlsx')
print("Data successfully read")

 # The dataframe with parent's income details
parent_inc = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_parent_income.xlsx')
print("Data successfully read")

# merge operation
print("merging")
moth_det = pd.merge(moth_qual,moth_occ,how= 'outer',on ='EMIS_NO')
print("merging")
fat_det = pd.merge(fath_qual,fath_occ,how= 'outer',on ='EMIS_NO')
print("merging")
parent_det = pd.merge(moth_det,fat_det,how= 'outer',on ='EMIS_NO')
print("merging")
parent_det_inc = pd.merge(parent_det,parent_inc,how= 'outer',on ='EMIS_NO')
print("merging")

sslc_data = pd.merge(govt,parent_det_inc,how= 'left',on ='EMIS_NO')

# To save as excel file
print("saving")
directory_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('data_preperation_10_pvt')
file_utilities.save_to_excel({'Report':sslc_data},'pvt.xlsx', dir_path=directory_path)


