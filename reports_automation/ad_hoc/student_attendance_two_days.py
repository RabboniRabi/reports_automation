"""
Module to create report for teacher attendance over two days
"""
import sys
sys.path.append('../')
import functools as ft
import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.format_utilities as format_utilities
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols
import excel2img
import os
import numpy as np


# Define the grouping levels and aggregation dictionary
grouping_levels = [cols.district_name]
grouping_agg_dict = {
    cols.tot_marked: 'sum',
    cols.tot_unmarked: 'sum'
    }

def _process_data(df_section_master, df_unmarked_sections,df_working_schools):

    """
    A for-loop that will create a new raw data file that will create a list of sections for each date for all the
    dates mentioned in the unmarked schools data frame
    """
    raw_data = []

    for label, df_unmarked_sections in df_unmarked_sections:




        data_frames_merge = [df_section_master, df_unmarked_sections, df_working_schools]

        data_final = ft.reduce(lambda left, right: pd.merge(left, right, how='left', on=), data_frames_merge)


    # Merging the data with the total schools count from the SQL query above (from df_report)
    df_grouped = pd.merge(df_schools, df_grouped, on=[cols.district_name])

    # Rename columns total marked and total marked to total marked and unmarked schools as data is now grouped
    df_grouped.rename(columns={cols.district_name: cols.district, cols.distinct_udise_count: cols.tot_schools},
                      inplace=True)

    # Change Total schools format to integer
    df_grouped['Total Schools'].astype(int)

    # Adding the % Marked Column
    df_grouped[cols.perc_marked_schls] = df_grouped['Grand Total']/df_grouped['Total Schools']

    # Sort the data by % highest marked schools
    df_grouped.sort_values([cols.perc_marked_schls], ascending=True, inplace=True)

    return df_grouped


def _format_report(df_report, df_data,):
    """
    Internal function to format the report and save

    Parameters:
    ----------
    df_report: Pandas DataFrame
        The report to be formatted
    """

    df_sheet_dict = {'School Marking': df_report, 'Raw Data': df_data}

    # Write the file on to the excel from the second row
    writer = file_utilities.get_xlsxwriter_obj(df_sheet_dict, 'Teacher_attendance_2_days.xlsx',
                                               file_utilities.get_curr_day_month_gen_reports_dir_path(),
                                               start_row=1)

    # Add borders, alignment, and text wrap to the whole data frame
    border_format = {'border': 1, 'align': 'center', 'text_wrap': True}
    format_utilities.apply_frmt_cols(writer, 'School Marking', 0, 4, border_format)

    # Apply colour gradient for % Marked column
    gradient_color_frmt = {'type': '3_color_scale'}
    col_index = df_report.columns.get_loc(cols.perc_marked_schls)
    format_utilities.apply_cond_frmt(writer, 'School Marking', col_index, gradient_color_frmt, 41)

    # Adding a heading with the variable dates based on the previous 2 days
    worksheet = writer.sheets['School Marking']
    day1 = df_report.columns[2].strftime('%d.%m.%y')
    day2 = df_report.columns[6].strftime('%d.%m.%y')

    # Merge the cells to form the heading
    worksheet.merge_range('A1:I1', "% Schools marking teacher attendance from {} to {}".format(day1, day2))

    # Apply formatting for heading
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    cell_format = workbook.add_format({'bold': True, 'align': 'vcenter', 'font_size': '11.4', 'valign': 'center'})
    worksheet.set_row(0, 18, cell_format)

    # Edit the names for the column labels and format them
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    column_format = workbook.add_format({'bold': True, 'align': 'vcenter', 'font_size': '11', 'bg_color': 'silver',
                                         'border': 1, 'text_wrap': True, 'valign': 'center', 'num_format': 'dd.mm.yy'})

    worksheet.write_row("A2:I2", df_report.columns.to_list(), column_format)

    # Edit the names for the 'Grand Total' row by adding the sum and average formula in cells and format it
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    column_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'font_size': '11', 'bg_color': 'silver', 'border': 1})

    worksheet.write_row("A41:I41", ['Grand Total', '=SUM(B3:B40)', '=SUM(C3:C40)', '=SUM(D3:D40)',
                        '=SUM(E3:E40)', '=SUM(F3:F40)', '=SUM(G3:G40)', '=SUM(H3:H40)', '=AVERAGE(I3:I40)'],
                        column_format)

    # Re-enter and format the Grand Total % Marked Cell specifically
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    column_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'font_size': '11', 'bg_color': 'silver', 'border': 1, 'num_format': '0.00%'})

    worksheet.write_row("I41", ['=AVERAGE(I2:I40)'], column_format)

    # Apply percentage formatting to % Marked column
    prcnt_frmt = {'num_format': '0.00%', 'text_wrap': True, 'align': 'center', 'bold': True, 'border': 1}
    comp_schools_col_index = df_report.columns.get_loc(cols.perc_marked_schls)
    format_utilities.apply_frmt_cols(writer, 'School Marking', comp_schools_col_index, comp_schools_col_index,
                                     prcnt_frmt, width=10)

    # Edit the column width for the rest of the columns
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    worksheet.set_column('B:H', 10)

    border_format = {'border': 1, 'align': 'center', 'valign': 'center'}
    format_utilities.apply_frmt_cols(writer, 'School Marking', 0, 7, border_format)

    # Edit the column width for the District Column
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    worksheet.set_column('A:A', 20, workbook.add_format(border_format))

    # Save the file
    writer.save()

    # Name the image, establish the file path and export the excel range as an image
    file_name = "teacher_marked_attendance_{}_to_{}.png".format(day1, day2)
    output_image = os.path.join(file_utilities.get_curr_day_month_gen_reports_dir_path(), file_name)
    # Get the file path of saved file to save PNG in same location
    file_path = file_utilities.get_file_path('Teacher_attendance_2_days.xlsx',
                                             file_utilities.get_curr_day_month_gen_reports_dir_path())
    excel2img.export_img(file_path, output_image, "School Marking", "A1:I41")


def run():
    """
    Main function that calls other functions to generate the report
    """

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the master list of sections currently active in the database
    df_section_master = dbutilities.fetch_data_as_df(credentials_dict, 'section_master_for_govt_aided_attendance.sql')

    # Get the total unmarked sections abstract from the SQL query file
    df_unmarked_sections = dbutilities.fetch_data_as_df(credentials_dict, 'unmarked _sections.sql')

    # Get the list of working schools from the SQL query file
    df_working_schools = dbutilities.fetch_data_as_df(credentials_dict, 'school_working_status.sql')



    # Process the data and get the report
    df_report = _process_data(df_data, df_unmarked_sections,df_working_schools)

    # Format the report and save
    _format_report(df_report, df_data)


if __name__ == "__main__":
    run()
