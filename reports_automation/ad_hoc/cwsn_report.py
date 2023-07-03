"""
Module to use the CWSN report available in the dashboard to create a report with
 - Block wise count of total students
 - Block wise count of students in school
 - Block wise count of students in common pool
 - Block wise count of students with NIDs
 - Block wise count of students with approved UDIDs
 - Block wise count of students with pending UDID applications - applied through website
 - Block wise count of students with pending UDID applications - applied through mobile

 - Block wise count of students attending schools
 - Block wise count of students attending SRPs (IE) centres
 - Block wise count of home based students
"""


import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.utilities as utilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import pandas as pd


def get_grouping_level_wise_student_count(df, group_levels, student_count_col):
    """
    Function to get the grouping levels wise count of CWSN students

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    student_count_col: str
        The column to count
    Returns:
    --------
    DataFrame object with group level wise count of total CWSN students
    """

    df_grouped = df.groupby(group_levels,sort=False)[student_count_col].count().reset_index()

    df_grouped.rename(columns={student_count_col: 'Total CWSN Students'}, inplace=True)

    return df_grouped

def get_grouping_level_wise_IDs_issued_count(df, group_levels, columns_regex_dict):
    """
    Function to get the grouping levels wise count of students with disability IDs.

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    columns_regex_dict: dict
        A column - regex of accepted values key - value pair dictionary
        This dictionary will be used to filter values in the ID columns by matching only the values
        given in the regex
        eg: {
            'col_a' : '[1-9].',
            'col_b' : '(a|h|e)+
        }           
    Returns:
    --------
    DataFrame object with group level wise count of students with disability ids
    """

    # Drop missing values in IDs
    df = df.dropna(subset=columns_regex_dict.keys())

    df_filtered_grouped = utilities.filter_group_count_valid_values(df, group_levels, columns_regex_dict)

    return df_filtered_grouped

def get_grouping_level_wise_UDID_app_count(df, group_levels, udid_col, appl_cat_regex_dict):
    """
    Function to get count of application modes of the pending UDID applications
    at each grouping level.
    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    udid_col: str
        The name of the column with UDID values    
    appl_cat_regex_dict: dict
        A application category - regex of accepted values key - value pair dictionary
        This dictionary will be used to filter values in the UDID column by matching only the values
        given in the regex
        eg: {
            'cat_a' : '[1-9].',
            'cat_b' : '(a|h|e)+
        }           
    Returns:
    --------
    DataFrame object with count of grouping level wise count of application modes
    """
    # Drop missing values in IDs
    df = df.dropna(subset=[udid_col])

    # Group the data by grouping level before filtering and keep
    df_grouped = df.groupby(group_levels, sort=False)[udid_col].count().reset_index()

    first_iteration = True
    for appl_category in appl_cat_regex_dict.keys():
        # Get the data filtered by application category
        df_appl_category = utilities.filter_df_by_regex_match(df, udid_col, appl_cat_regex_dict[appl_category])
        # Group the data to grouping level
        df_appl_category_grouped = df_appl_category.groupby(group_levels, sort=False)[udid_col].count().reset_index()
        #df_appl_category_grouped = df_appl_category.groupby(group_levels, sort=False)[udid_col].count().unstack(fill_value=0).stack().reset_index()
        # Rename the udid column to application cateogry name
        df_appl_category_grouped.rename(columns = {udid_col: appl_category}, inplace = True)

        # Do a Vlookup match with above result by lowest grouping level and fill empty results with 0.
        # Groupby will omit rows where the count is zero for udid_col column. 
        # To include the data with zero counts, a Vlookup is done with the grouped data before filtering was done.
        # Where there is no entry for a row in the above grouping, zero is inserted
        lowest_grouping_level = group_levels[len(group_levels) - 1]
        df_grouped[appl_category] = df_grouped[lowest_grouping_level].apply(utilities.xlookup,\
         args=(df_appl_category_grouped[lowest_grouping_level], df_appl_category_grouped[appl_category], 0))     

    return df_grouped


def main():

    # Read report from excel
    #df_report = pd.read_excel(r'/home/rabboni/Downloads/CWSN-Report.xlsx', sheet_name='Report', skiprows=4)
    # Ask the user to select the CWSN report excel file.
    cwsn_report = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(cwsn_report, sheet_name='Report', skiprows=4)
    # Rename the column names to standard format
    df_report = column_cleaner.standardise_column_names(df_report)

    # List of student statuses to count
    student_statuses = [cols.cwsn_in_School, cols.cwsn_cp]
    # List of columns with student IDs
    id_columns = [cols.nid, cols.udid]
    # Levels to apply grouping by
    group_levels = [cols.district_name]
    # List of places student is supported in
    supported_in_vals = [cols.cwsn_school_ie, cols.cwsn_school, cols.cwsn_home_based, cols.cwsn_home_ie]

    id_columns_regex_dict = {
        # Accept only 5 to 6 digits or values starting with TN and ends with range of 3 to 6 digits.
        cols.nid: '(^[0-9]{5,6}$)|(^TN[\s\S][a-z]{2,5}[\s\S][a-z]{2,5}[\s\S][0-9]{3,6}$)|(^TN[\s\S][a-z]{2,5}[\s\S][a-z]{2,5}[\s\S][0-9]{3,6}[\s\S][0-9]{2,4}$)',
        # Accept only values starting with TN
        cols.udid: '(?i)^TN.*$'
    }

    appl_cat_regex_dict = {
        cols.web: '^33([0-9]{18})$', # Website application numbers will have 20 digits and start with 33
        cols.mobile: '([0-9]{6})' # Mobile application number will contain 6 digits
    }

    # Get block level wise total students count
    block_wise_total_students_count = get_grouping_level_wise_student_count (df_report, group_levels, cols.cwsn_name)

    # Get the block level wise count of students in school and in common pool
    block_wise_status_count = utilities.get_grouping_level_wise_col_values_count(
        df_report, group_levels, cols.cwsn_status, student_statuses)
    
    # Get block level wise count of valid student IDs
    block_wise_IDs_issued_count = get_grouping_level_wise_IDs_issued_count(df_report, group_levels, id_columns_regex_dict)
    
    # Get block level wise count of pending UDID applications in different modes
    block_wise_appl_categories_count = get_grouping_level_wise_UDID_app_count(df_report, group_levels, 'UDID', appl_cat_regex_dict)
    
    # Get block level wise count of supported categories
    block_wise_supp_cat_wise_count = utilities.get_grouping_level_wise_col_values_count(
        df_report, group_levels, 'SupportedIn', supported_in_vals )

    block_wise_has_account_count = pd.pivot_table(df_report, index=group_levels, columns=cols.cwsn_has_acct,
                aggfunc='size', fill_value=0, sort=False).reset_index()    
    
    # Merge the results into one block level summary
    df_overview = block_wise_total_students_count.merge(block_wise_status_count[group_levels+student_statuses])
    df_overview = df_overview.merge(block_wise_supp_cat_wise_count[group_levels+supported_in_vals])
    df_overview = df_overview.merge(block_wise_IDs_issued_count[group_levels+id_columns])
    df_overview = df_overview.merge(block_wise_appl_categories_count[group_levels + list(appl_cat_regex_dict.keys())])
    df_overview = df_overview.merge(block_wise_has_account_count[group_levels + ['Yes', 'No']])
    

    # Rename columns for better readability
    df_overview.rename(columns = {
        cols.cwsn_in_School: cols.stdnts_in_school,
        cols.cwsn_cp: cols.stdnts_in_cp,
        cols.nid: cols.nid_count,
        cols.udid: cols.udid_count,
        cols.cwsn_school_ie: cols.cwsn_stu_school_ie,
        cols.cwsn_school: cols.cwsn_school_stu,
        cols.cwsn_home_based: cols.cwsn_home_based_stu,
        cols.cwsn_home_ie: cols.cwsn_stu_home_ie,
        cols.web: cols.pending_web_applications,
        cols.mobile: cols.pending_mob_applications,
        cols.yes_col: cols.with_acct,
        cols.no_col: cols.witht_acct
        }, inplace=True)

    # Sort the values
    df_overview.sort_values(group_levels, inplace = True)    

    dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
    file_utilities.save_to_excel({'Report':df_overview}, 'CWSN_Summary.xlsx', dir_path=dir_path)

if __name__ == "__main__":
    main()