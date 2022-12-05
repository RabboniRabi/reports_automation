"""

Module with functions to:
    -Will report the completion rate of the Ennum Ezhuthum Summative Assessment for each district
"""
import sys
sys.path.append('../')

import utilities.utilities as utilities
import functools as ft
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.ranking_utilities as ranking_utilities
import utilities.report_utilities as report_utilities


import pandas as pd
import os
from datetime import date
from pathlib import Path

"""
Step 0:
Define the all the variables in the report

"""

"-----------------------------------------------------------------------------------------------------------------------"
# Step 0:
# Global variables
# Column names are defined here so that they can be edited in one place
total_student_count  = 'total'
students_ageing30_count = 'last_30days'
district_name = 'district_name'
udise_col = 'udise_code'
school_name ='school_name'
edu_district_name = 'edu_dist_name'
block_name = 'block_name'
school_category = 'category'
school_level = 'school_level'
class_number = 'class'
beo_user = 'beo_user'
beo_name ='beo_name'
deo_user_elm = 'deo_name (elementary)'
deo_user_sec = 'deo_name (secondary)'
cwsn_students ='cwsn'
beo_rank = 'BEO Rank'
deo_rank_elm = 'DEO Rank Elementary'
deo_rank_sec = 'DEO Rank Secondary'
perc_students_cp = '% Students ageing > 30 days'
total_cwsn_students ='cwsn'
total_cp_students ='total'
school_type ='school_type'
subjects='subjects'
#Class 1


cls1_tot = 'Class1 Total student'
cls1_assess ='Class 1 Assessed'
cls1_long_abs = 'Cls1 Long Absent'
cls1_cwsn = 'Cls1 Cwsn'

#Class 2
cls2_tot = 'Class2 Total student'
cls2_assess ='Class 2 Assessed'
cls2_long_abs = 'Cls2 Long Absent'
cls2_cwsn = 'Cls2 Cwsn'

#Class 3
cls3_tot = 'Class3 Total student'
cls3_assess ='Class 3 Assessed'
cls3_long_abs = 'Cls3 Long Absent'
cls3_cwsn = 'Cls3 Cwsn'

cls1_cmpltd = 'class 1 completed'
cls2_cmpltd = 'class 2 completed'
cls3_cmpltd = 'class 3 completed'

# Dictionary to define how the values to merge on and the how the merge will work.
merge_dict = {
    'on_values' : [district_name,block_name,school_name,udise_col],
    'how' : 'left'
}
# Column order the final report will display
col_order = [district_name,deo_user_sec,deo_user_elm,school_level,school_category,cls1_assess,cls1_tot,cls2_assess,cls2_tot,
             cls3_assess,cls3_tot,cls3_assess,'Total Assessed','Total Assessed']

# Define aggregate dictionary for summarising raw data
summarize_dict = {
    cls1_assess: 'sum',
    cls1_tot: 'sum',
    cls2_assess: 'sum',
    cls2_tot: 'sum',
    cls3_assess: 'sum',
    'Total Students': 'sum',
    'Total Assessed': 'sum'}

ranking_args_dict = {
    'agg_dict': summarize_dict,
    'ranking_val_desc': '% Summative Assessment Completion',
    'num_col': 'Total Assessed',
    'den_col': 'Total Students',
    'sort': True,
    'ascending': False
}
"-----------------------------------------------------------------------------------------------------------------------"



def main():

    """""
    #code for running the sql script:

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    df_report = dbutilities.fetch_data_as_df(credentials_dict, 'common_pool_latest.sql')

    print('df_report fetched from db: ', df_report)
    """

    ee_sa_basefile = file_utilities.user_sel_excel_filename()
    raw_data = pd.read_excel(ee_sa_basefile, sheet_name='Report')

    cols = raw_data.columns.drop([district_name,edu_district_name,block_name,udise_col,school_name,subjects])
    raw_data.drop(columns=[edu_district_name], axis=1, inplace=True)
    raw_data[cols] = raw_data[cols].apply(pd.to_numeric, errors='coerce')
    raw_data = raw_data.groupby([district_name,block_name,udise_col,school_name]).mean().round(0).reset_index()
    raw_data[cls1_tot] = raw_data[cls1_tot] - (raw_data[cls1_long_abs]+raw_data[cls1_cwsn])
    raw_data[cls2_tot] = raw_data[cls2_tot] - (raw_data[cls2_long_abs]+raw_data[cls2_cwsn])
    raw_data[cls3_tot] = raw_data[cls3_tot] - (raw_data[cls3_long_abs]+raw_data[cls3_cwsn])
    raw_data = raw_data.drop(columns = [cls1_long_abs,cls1_cwsn,cls2_long_abs,cls2_cwsn,cls3_long_abs,cls3_cwsn])
    raw_data[cls1_cmpltd] = raw_data[cls1_assess]/raw_data[cls1_tot]
    raw_data[cls2_cmpltd] = raw_data[cls2_assess]/raw_data[cls2_tot]
    raw_data[cls3_cmpltd] = raw_data[cls3_assess]/raw_data[cls3_tot]
    raw_data['Total Students'] = raw_data[cls1_tot]+raw_data[cls2_tot]+raw_data[cls3_tot]
    raw_data['Total Assessed'] = raw_data[cls1_assess]+raw_data[cls2_assess]+raw_data[cls3_assess]



    # Update the data with the BRC-CRC mapping
    data_with_brc_mapping = report_utilities.map_data_with_brc(raw_data, merge_dict)
    data_with_brc_mapping.replace('Null', value=0, inplace=True)
    data_with_brc_mapping = data_with_brc_mapping[~data_with_brc_mapping[school_level].isin([0])]

    #list_touse =  list(set(brc_crc_master_sheet.columns.to_list() + raw_data.columns.to_list()))
    #print(list_touse)

    # Data re-structure, groupby

    data_final = data_with_brc_mapping.groupby([district_name,deo_user_sec,deo_user_elm,school_level,school_category])\
        .aggregate(summarize_dict).reset_index()
    file_utilities.save_to_excel({'test1':data_with_brc_mapping,'test2':data_final},'test1.xlsx')

    # Post creating data summary
    # Get the elementary report

    elem_report = report_utilities.get_elementary_report((data_final.drop(deo_user_sec,axis=1).drop_duplicates(subset=[deo_user_elm,school_category])), 'percent_ranking', ranking_args_dict, 'EE_SA', 'Ennum Ezhuthum')
    sec_report = report_utilities.get_secondary_report((data_final.drop(deo_user_elm,axis=1).drop_duplicates(subset=[deo_user_sec,school_category])), 'percent_ranking', ranking_args_dict, 'EE_SA', 'Ennum Ezhuthum')


    file_utilities.save_to_excel({'EE_SA_Elm': elem_report}, 'EE_SA_Elm.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())

    file_utilities.save_to_excel({'EE_SA_Sec': sec_report}, 'EE_SA_Sec.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())

if __name__ == "__main__":
    main()

