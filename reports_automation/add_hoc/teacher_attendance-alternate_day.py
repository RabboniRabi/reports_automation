from datetime import datetime
from datetime import timedelta
import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.format_utilities as format_utilities
import utilities.dbutilities as dbutilities
import excel2img
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import pandas as pd

groupby_index = ['district_name']
groupby_criteria = {"totalmarked":"sum","totalunmarked":"sum"}

# Read the database connection credentials
credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

# Get the latest students and teachers count
df_report = dbutilities.fetch_data_as_df(credentials_dict, 'teacher_attendance_last2days.sql')

#groupby district - keep this variable to add block if necessary - and sum marked and unmarked and % calc
df_filtered = df_report.groupby(groupby_index).agg(groupby_criteria).reset_index()

df_filtered.rename(columns={'totalmarked': 'Marked Schools','totalunmarked':'Unmarked Schools','district_name':'District'}, inplace=True)

df_filtered['Total Schools'] = df_filtered['Marked Schools']+df_filtered['Unmarked Schools']
df_filtered['% Marked'] =  df_filtered['Marked Schools']/df_filtered['Total Schools']


#sortby highest unmarked
df_filtered=df_filtered.sort_values(['% Marked'],ascending=True)


function_dict = {"Marked Schools": "sum","Unmarked Schools":"sum"
                 ,"Total Schools":"sum","% Marked":"mean"}
df_filtered.loc[-1,:] = df_filtered.aggregate(function_dict)

df_filtered.at[-1, 'District'] = "Grand Total"

# Pandas formatting - colour gradient and borders

df_formatted = df_filtered.style.set_properties(**{'text-align': 'center','border-color':'black','border-width':'0.1em'})

df_formatted.set_table_styles([dict(selector='th', props=[('text-align', 'center','border-color','Black','border-width','0.1em')])])


#datatoexcel = pd.ExcelWriter(r'C:\Users\Admin\Downloads\teachtest.xlsx', engine='xlsxwriter')
"""
df_formatted.to_excel(datatoexcel, sheet_name='School Marking',index=False)
# save the excel
datatoexcel.save()


df_final = openpyxl.load_workbook('C:/Users/Admin/Downloads/teachtest.xlsx')
main_page = df_final['School Marking']
main_page.insert_rows(idx=0,amount=1)"""

# Get an XLSX Writer object to apply formatting
df_sheet_dict = {
    'School Marking': df_filtered,
}
writer = file_utilities.get_xlsxwriter_obj(df_sheet_dict, 'C:/Users/Admin/Downloads/teachtest.xlsx')


border_format = {'border' : 1,'align':'center','text_wrap':True}
format_utilities.apply_frmt_cols(writer, 'School Marking', 0, 4, border_format)

# Apply colour gradient for % Marked column
gradient_color_frmt = {'type': '3_color_scale'}
col_index = df_filtered.columns.get_loc('% Marked')
no_of_rows = df_filtered.shape[0]
format_utilities.apply_cond_frmt(writer, 'School Marking', col_index, gradient_color_frmt, no_of_rows)


# Apply percentage formatting to % Marked column
prcnt_frmt = {'num_format': '0.00%','text_wrap':True}
comp_schools_col_index = df_filtered.columns.get_loc('% Marked')
format_utilities.apply_frmt_cols(writer, 'School Marking', comp_schools_col_index, comp_schools_col_index,
                                 prcnt_frmt)

worksheet = writer.sheets['School Marking']
worksheet.set_column(0,4,19)


# Set cell borders

writer.save()


excel2img.export_img("C:/Users/Admin/Downloads/teachtest.xlsx","C:/Users/Admin/Downloads/teachtest.png","School Marking","A1:E40")



"""# First Row
day1 =(datetime.today() - timedelta(days=2)).strftime('%m/%d/%Y')
day2 = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')
main_page['A1'].value = '% of Schools marking Teacher Attendance from {} to {}'.format(day1,day2)
font1 = Font(size=12, bold=True)
main_page['A1'].font = font1
main_page.merge_cells('A1:F1')
alignment=Alignment(horizontal='center',vertical='center')
main_page['A1'].alignment = alignment
bd=Side(border_style='thin',color='00000000')
border=Border(top=bd,left=bd,right=bd,bottom=bd)


df_final.save('C:/Users/Admin/Downloads/teachtest.xlsx')"""

