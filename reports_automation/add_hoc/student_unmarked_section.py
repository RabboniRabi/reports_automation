from datetime import datetime
from datetime import timedelta
import sys
sys.path.append('../')
import utilities.dbutilities as dbutilities
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import pandas as pd

#Dictionary for groupby criteria
Total_Schools = "school_name"
groupby_index = ['district_name']
groupby_criteria = {"udise_code":"count"}

# Read the database connection credentials
credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

# Get the latest sections unmarked details from the SQL query file
df_report = dbutilities.fetch_data_as_df(credentials_dict, 'students_unmarked_weekly.sql')

#Drop the unneccesary rows
df_report = df_report.drop(columns=['c','edate'])

#Get the total sections abstract from the SQL query file
df_sections = dbutilities.fetch_data_as_df(credentials_dict, 'total_sections.sql')

#groupby district - keep this variable to add block if necessary - and sum marked,partially marked and unmarked and % calculation
df_filtered = df_report.groupby(groupby_index).agg(groupby_criteria).reset_index()

# Merging the data with the total sections count from the SQL query above (from df_report)
df_filtered = pd.merge(df_filtered,df_sections,on=['district_name'])

#Renaming columns to the appropriate name
df_filtered.rename(columns={'district_name':'District',"count(section)":"Total Sections","udise_code":"Unmarked Sections"},
                                inplace=True)

#Getting percentage column
df_filtered['% Unmarked Sections for 7 days'] = df_filtered['Unmarked Sections']/df_filtered['Total Sections']

#Sorting the column based on highest number of sections unmarked in a district
df_filtered=df_filtered.sort_values(['% Unmarked Sections for 7 days'],ascending=False)


# Adding the grand total row
function_dict = {"Total Sections":"sum","Unmarked Sections":"sum","% Unmarked Sections for 7 days":"mean"}
df_filtered.loc[-1,:] = df_filtered.aggregate(function_dict)

df_filtered.at[-1, 'District'] = "Grand Total"

# Changing the format from float to percentage
df_filtered.loc[:, '% Unmarked Sections for 7 days'] = df_filtered['% Unmarked Sections for 7 days'].map('{:.2%}'.format)

#Adding borders and formatting to both the dataframes
df_filtered = df_filtered.style.set_properties(**{'text-align': 'center','border-color':'black','border-width':'0.1em'})
df_report = df_report.style.set_properties(**{'text-align': 'center','border-color':'black','border-width':'0.1em'})

# Saving the data to an excel sheet both the unmarked sections and the abstracted file
datatoexcel = pd.ExcelWriter(r'C:\Users\Admin\Downloads\Students Attendance-Unmarked Sections Report.xlsx', engine='xlsxwriter')

df_filtered.to_excel(datatoexcel, sheet_name='Unmarked Sections Abstract',index=False)
df_report.to_excel(datatoexcel,sheet_name='Unmarked Sections Detailed',index=False)
# save the excel
datatoexcel.save()

#Additional Formatting

# Adding a row to enter the title of the abstracted report
df_final = openpyxl.load_workbook('C:/Users/Admin/Downloads/Students Attendance-Unmarked Sections Report.xlsx')
main_page = df_final['Unmarked Sections Abstract']
main_page.insert_rows(idx=0,amount=1)

# First Row - Heading with the date from and date to and also formatting the same.
day1 =(datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
day2 = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')
main_page['A1'].value = '% of Schools not marking Student Attendance from {} to {}'.format(day1,day2)
font1 = Font(size=12, bold=True)
main_page['A1'].font = font1
main_page.merge_cells('A1:D1')
alignment=Alignment(horizontal='center',vertical='center')
main_page['A1'].alignment = alignment
bd=Side(border_style='thin',color='00000000')
border=Border(top=bd,left=bd,right=bd,bottom=bd)

# Final Save
df_final.save('C:/Users/Admin/Downloads/Students Attendance-Unmarked Sections Report.xlsx')
