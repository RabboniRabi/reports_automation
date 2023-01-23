"""
Module with functions to create report on RTE admission status
"""

import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.report_utilities as report_utilities
import pandas as pd
import os

# Declare column names to be used in the module
admitted_status = 'Admitted'
not_admitted_status = 'Not admitted'
alloted_status = 'Alloted'
wait_lst_status = 'Wait List'
allot_tot = 'Alloted Total'

def get_rte_admission_status_summary(df, group_levels, agg_col):
    """
    Function to summarise the number of schools with different admission and allotment statuses
    at given grouping levels. 

    Parameters:
    ----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    agg_col: str
        The name of the column to aggregate by    

    Returns:
    --------
    DataFrame object with summary of admission statuses schools count
    """

    # Get count of schools for different admission statuses
    df_admit_status_schools_count = pd.pivot_table(df, values=agg_col, index=group_levels,
                    columns=['Admit_Status'], aggfunc='count').reset_index()


    # Get the data summary for only 'Admitted' and 'Not admitted' statuses 
    df_admit_status_schools_count = df_admit_status_schools_count[group_levels + [admitted_status] + [not_admitted_status]]       


    # Get count of schools for different allotment statuses
    df_allot_status_schools_count = pd.pivot_table(df, values=agg_col, index=group_levels,
                    columns=['Allot_Status'], aggfunc='count').reset_index()

    # Get the count of schools with only 'Alloted' and 'Wait List' Statuses
    df_allot_status_schools_count  = df_allot_status_schools_count[group_levels + [alloted_status] + [wait_lst_status]]

    # replace the NA values in 'Wait List' status columns with 0
    df_allot_status_schools_count[wait_lst_status] = df_allot_status_schools_count[wait_lst_status].fillna(0)

    # Create a column called 'Alloted Total' whose row values are sum of values in 'Alloted and 'Wait List' cell values
    df_allot_status_schools_count[allot_tot] = df_allot_status_schools_count[alloted_status] + df_allot_status_schools_count[wait_lst_status]

    # Merge the admit and allot statuses data
    df_admission_status_summary = df_admit_status_schools_count.merge(df_allot_status_schools_count[group_levels + [allot_tot]])

    return df_admission_status_summary



def run():
    """
    Function to call other internal functions and create the RTE admission status report
    """

    # Read the database connection credentials
    #credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    #df_report = dbutilities.fetch_data_as_df(credentials_dict, 'rte_admission_status.sql')

    #print('df_report fetched from db: ', df_report)

    # Alternatively
    # Get the data from the source data folder
    print('file_utilities.get_source_data_dir_path(): ', file_utilities.get_source_data_dir_path())
    file_path = os.path.join(file_utilities.get_source_data_dir_path(), 'rte_admission_status_2022.xlsx')
    df_report = pd.read_excel(file_path, sheet_name='Report', skiprows=4)

    print('df_report columns: ', df_report.columns.to_list())

    group_levels = ['District', 'edu_dist_name', 'Block_Name']

    # Get the RTE admission status summary from raw data
    df_admission_status_summary = get_rte_admission_status_summary(df_report, group_levels, 'School_Name')

    # Prepare the data needed for generating the report
    ranking_args_dict = {
        'group_levels' : group_levels,
        'agg_cols' : ['class_1', 'Total'],
        'agg_func' : 'sum',
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : True, 
        'ascending' : False
    }
    # Get the Elementary report
    elem_report = report_utilities.get_elem_ranked_report(\
        df_admission_status_summary, 'percent_ranking', ranking_args_dict, 'RTE', 'Operations')

    # Save the elementary report
    file_utilities.save_to_excel({'Elementary Report': elem_report}, 'RTE_admn_status.xlsx',
            dir_path = get_curr_month_elem_ceo_rpts_dir_path())    

    # Get the Secondary report
    elem_report = report_utilities.get_sec_ranked_report(\
        df_admission_status_summary, 'percent_ranking', ranking_args_dict, 'RTE', 'Operations')    

    # Save the secondary report
    file_utilities.save_to_excel({'Secondary Report': elem_report}, 'RTE_admn_status.xlsx',
            dir_path = get_curr_month_secnd_ceo_rpts_dir_path()) 

    



if __name__ == "__main__":
    run()
