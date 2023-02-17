"""
Module to create report for teacher attendance over two days
"""

from datetime import datetime
from datetime import timedelta
import sys
import os

sys.path.append('../')
import utilities.format_utilities as format_utilities
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.column_names_utilities as cols
import excel2img


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
    #groupby district - keep this variable to add block if necessary - and sum marked and unmarked and % calc
    df_grouped = df_data.groupby(grouping_levels).agg(grouping_agg_dict).reset_index()
    # Rename columns total marked and total marked to total marked and unmarked schools as data is now grouped
    df_grouped.rename(columns={cols.tot_marked: cols.marked_schools, cols.tot_unmarked: cols.unmarked_schools,
                               cols.district_name:cols.district}, inplace=True)
    # Calculate total schools by summing the marked and unmarked schools
    df_grouped[cols.tot_schools] = df_grouped[cols.marked_schools] + df_grouped[cols.unmarked_schools]
    # Calculate % Marked schools
    df_grouped[cols.perc_marked_schls] =  df_grouped[cols.marked_schools] / df_grouped[cols.tot_schools]

    # Sort the data by % highest marked schools
    df_grouped.sort_values([cols.perc_marked_schls], ascending=True, inplace=True)

    # Define a columns aggregate function to calculate a grand total row at the bottom
    cols_agg_dict = {
        cols.marked_schools : 'sum',
        cols.unmarked_schools : 'sum',
        cols.tot_schools : 'sum', 
        cols.perc_marked_schls : 'mean'
        }

    df_grouped.loc[-1,:] = df_grouped.aggregate(cols_agg_dict)

    df_grouped.at[-1, cols.district] = "Grand Total"

    return df_grouped


def _format_report(df_report,df_data):
    """
    Internal function to format the report and save

    Parameters:
    ----------
    df_report: Pandas DataFrame
        The report to be formatted
    """


    # Open the file in OpenPyXl to apply some formatting using xlsxwriter
    file_path = file_utilities.get_file_path('Teacher_attendance_2_days.xlsx', file_utilities.get_curr_day_month_gen_reports_dir_path())

    df_sheet_dict = {'School Marking': df_report,'Raw Data':df_data}

    #Write the file on to the excel from the second row
    writer = file_utilities.get_xlsxwriter_obj(df_sheet_dict, 'Teacher_attendance_2_days.xlsx', file_utilities.get_curr_day_month_gen_reports_dir_path(),
                                               start_row=1)
    #Add borders, alignment, and text wrap to the whole data frame
    border_format = {'border': 1, 'align': 'center', 'text_wrap': True}
    format_utilities.apply_frmt_cols(writer, 'School Marking', 0, 4, border_format)


    # Apply colour gradient for % Marked column
    gradient_color_frmt = {'type': '3_color_scale'}
    col_index = df_report.columns.get_loc(cols.perc_marked_schls)
    format_utilities.apply_cond_frmt(writer, 'School Marking', col_index, gradient_color_frmt, 41)

    #Adding a heading with the variable dates based on the previous 2 days
    worksheet = writer.sheets['School Marking']
    day1 = (datetime.today() - timedelta(days=2)).strftime('%d.%m.%Y')
    day2 = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')

    #Merge the cells to form the heading
    worksheet.merge_range('A1:E1', "% Schools marking teacher attendance from {} to {}".format(day1,day2))

    #Apply formatting for heading
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    cell_format = workbook.add_format({'bold': True,'align':'vcenter','font_size':'11.62','valign':'center'})
    worksheet.set_row(0, 18, cell_format)

    #Edit the names for the column labels and format them
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    format = workbook.add_format({'bold': True,'align':'vcenter','font_size':'11','bg_color':'silver','border':1,'text_wrap':True
                                  ,'valign':'center'})

    worksheet.write_row("A2:F2", ['District', 'Marked Schools', 'Unmarked Schools','Total Schools','% Marked Schools'], format)

    #Edit the names for the 'Grand Total' row by adding the sum and average formula in cells and format it
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    format = workbook.add_format(
        {'bold': True, 'align': 'center', 'font_size': '11', 'bg_color': 'silver', 'border': 1})

    worksheet.write_row("A41:F41", ['Grand Total', '=SUM(B2:B40)', '=SUM(C2:C40)', '=SUM(D2:D40)', '=AVERAGE(E2:E40)'],
                        format)

    #Re-enter and format the Grand Total % Marked Cell specifically
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    format = workbook.add_format(
        {'bold': True, 'align': 'center', 'font_size': '11', 'bg_color': 'silver', 'border': 1,'num_format': '0.00%'})

    worksheet.write_row("E41", ['=AVERAGE(E2:E40)'],
                        format)

    # Apply percentage formatting to % Marked column
    prcnt_frmt = {'num_format': '0.00%', 'text_wrap': True,'align':'center','bold':True,'border':1}
    comp_schools_col_index = df_report.columns.get_loc(cols.perc_marked_schls)
    format_utilities.apply_frmt_cols(writer, 'School Marking', comp_schools_col_index, comp_schools_col_index,
                                     prcnt_frmt, width=10)
    #Edit the column width for the District Column
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    worksheet.set_column('A:A',20)

    #Edit the column width for the rest of the columns
    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name('School Marking')
    worksheet.set_column('B:D',10)

    #Save the file
    writer.save()

    #Name the image, establish the file path and export the excel range as an image
    file_name = "teacher_marked_attendance_{}_to_{}.png".format(day1,day2)
    output_image = os.path.join(file_utilities.get_curr_day_month_gen_reports_dir_path(), file_name)
    excel2img.export_img(file_path, output_image, "School Marking", "A1:E41")


def run():
    """
    Main function that calls other functions to generate the report
    """

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    df_data = dbutilities.fetch_data_as_df(credentials_dict, 'teacher_attendance_last2days.sql')

    # Process the data and get the report
    df_report = _process_data(df_data)

    # Format the report and save
    _format_report(df_report, df_data)



if __name__ == "__main__":
    run()





