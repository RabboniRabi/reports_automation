"""
Module to create report for teacher attendance over two days
"""

from datetime import datetime
from datetime import timedelta
import sys

sys.path.append('../')

import utilities.format_utilities as format_utilities
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.column_names_utilities as cols

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import pandas as pd

# Define the grouping levels and aggregation dictionary
grouping_levels = [cols.district_name]
grouping_agg_dict = {
    cols.tot_marked : 'sum',
    cols.tot_unmarked : 'sum'
    }


def _process_data(df_data):
    """
    Internal function to process the data to generate the report
    
    Parameters:
    -----------
    df_data: Pandas DataFrame
        The data as a Pandas DataFrame object

    Returns:
    -------
    The data processed as a report.
    """
    print('df_data: ', df_data)
    #groupby district - keep this variable to add block if necessary - and sum marked and unmarked and % calc
    df_grouped = df_data.groupby(grouping_levels).agg(grouping_agg_dict).reset_index()
    # Rename columns total marked and total marked to total marked and unmarked schools as data is now grouped
    df_grouped.rename(columns={cols.tot_marked: cols.tot_marked_schls, cols.tot_unmarked: cols.tot_unmarked_schls}, inplace=True)
    # Calculate total schools by summing the marked and unmarked schools
    df_grouped[cols.tot_schools] = df_grouped[cols.tot_marked_schls] + df_grouped[cols.tot_unmarked_schls]
    # Calculate % Marked schools
    df_grouped[cols.perc_marked_schls] =  df_grouped[cols.tot_marked_schls] / df_grouped[cols.tot_schools]

    # Sort the data by % highest marked schools
    df_grouped.sort_values([cols.perc_marked_schls], ascending=True, inplace=True)

    # Define a columns aggregate function to calculate a grand total row at the bottom
    cols_agg_dict = {
        cols.tot_marked_schls : 'sum',
        cols.tot_unmarked_schls : 'sum',
        cols.tot_schools : 'sum', 
        cols.perc_marked_schls : 'mean'
        }

    df_grouped.loc[-1,:] = df_grouped.aggregate(cols_agg_dict)

    df_grouped.at[-1, 'District'] = "Grand Total"

    print('df_grouped: ', df_grouped)

    return df_grouped


def _format_report(df_report):
    """
    Internal function to format the report and save

    Parameters:
    ----------
    df_report: Pandas DataFrame
        The report to be formatted
    """

    # Set the text alignment, border and colour gradient using Pandas
    df_formatted = df_report.set_properties(**{'text-align': 'center','border-color':'black','border-width':'0.1em'}).\
    background_gradient(cmap='RdYlGn',subset=cols.perc_marked_schls)

    df_formatted.set_table_styles([dict(selector='th', props=[('text-align', 'center','border-color','Black','border-width','0.1em')])])

    # Save the data
    file_utilities.save_to_excel({'School Marking': df_formatted}, 'Teacher_attendance_2_days.xlsx', \
            dir_path=file_utilities.get_curr_day_month_gen_reports_dir_path(), engine='xlsxwriter')
    
    #data_to_excel = pd.ExcelWriter(r'C:\Users\Admin\Downloads\teachtest.xlsx', engine='xlsxwriter')
    #df_formatted.to_excel(data_to_excel, sheet_name='School Marking',index=False)
    #data_to_excel.save()

    # Open the file in OpenPyXl to apply some formatting using OpenPyXl
    file_path = file_utilities.get_file_path('Teacher_attendance_2_days.xlsx', file_utilities.get_curr_day_month_gen_reports_dir_path())
    df_final = openpyxl.load_workbook(file_path)
    main_page = df_final['School Marking']
    main_page.insert_rows(idx=0,amount=1)

    prcnt_frmt = {'num_format': '0.00%'}
    comp_schools_col_index = df_formatted.columns.get_loc('% Fully completed')
    format_utilities.apply_frmt_cols(df_formatted, 'Schools screening status', comp_schools_col_index, comp_schools_col_index,
                                    prcnt_frmt)

    # First Row
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


    df_final.save(file_path)

def run():
    """
    Main function that calls other functions to generate the report
    """

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials_attendance.json')

    # Get the latest students and teachers count
    df_data = dbutilities.fetch_data_as_df(credentials_dict, 'teacher_attendance_last2days.sql')

    # Process the data and get the report
    df_report = _process_data(df_data)

    # Format the report and save
    _format_report(df_report)



if __name__ == "__main__":
    run()





