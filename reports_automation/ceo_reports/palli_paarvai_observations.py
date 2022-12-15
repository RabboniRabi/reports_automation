"""

Module with functions to:
    -Will report the % of observations conducted vs the target no.of observations to be conducted by the CEOs and DEOs
"""
import sys
sys.path.append('../')

import utilities.utilities as utilities
import functools as ft
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import utilities.ranking_utilities as ranking_utilities
import utilities.report_utilities as report_utilities
from datetime import datetime
import utilities.column_names_utilities as cols


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
observation_date  = 'Date of Observation'
designation_user_id = 'Observed by'
designation = 'stackholders'
district_name = 'district_name'
udise_col = 'udise_code'
school_name ='School_Observed'
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
school_type ='school_type'
edu_dist_id = 'edu_dist_id'
deo_target = 'deo_target'
ceo_target ='ceo_target'
management = 'management'


# Dictionary to define how the values to merge on and the how the merge will work.
merge_dict = {
    'on_values' : [district_name, udise_col],
    'how' : 'left'
}
ranking_args_dict = {
    'agg_dict': 'sum',
    'ranking_val_desc': '% Overall Observation Completion',
    'num_col': 'DEO',
    'den_col': deo_target,
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

    # Getting the raw data
    ee_sa_basefile = file_utilities.user_sel_excel_filename()
    raw_data = pd.read_excel(ee_sa_basefile, sheet_name='Report',skiprows=4)
    #raw data only for the specific month we need - previous month
    raw_data[observation_date] = raw_data[observation_date].dt.month
    raw_data =raw_data[raw_data[observation_date] == (datetime.now().month-1)]
    #taking only the ceo and deo observations
    raw_data = raw_data[raw_data['Observed by'].str.contains('|'.join(['ceo','deo']))]
    raw_data = raw_data[~(raw_data[designation] == 'Null')]

    data_with_brc_mapping = report_utilities.map_data_with_brc(raw_data, merge_dict)
    data_with_brc_mapping.replace('Null', value=0, inplace=True)
    data_with_brc_mapping = data_with_brc_mapping[~data_with_brc_mapping[school_level].isin([0])]

    data_final_elm = pd.pivot_table(data_with_brc_mapping,index=[district_name,deo_user_elm,school_level,school_category],columns=designation,values=udise_col
                    ,aggfunc='count').reset_index().fillna(0)

    data_final_sec = pd.pivot_table(data_with_brc_mapping, columns=designation, values=udise_col,
                                    index=[district_name,deo_user_sec,school_level,school_category], aggfunc='count').fillna(0).reset_index()

    #targets are 12 for both the designations
    #merging both target and raw data
    data_final_elm[deo_target] = 6
    data_final_elm['% School Observations by DEOs'] = data_final_elm['DEO']/data_final_elm[deo_target]
    data_final_elm[ceo_target] = 3
    data_final_elm['% School Observations by CEOs'] = data_final_elm['CEO']/data_final_elm[ceo_target]
    data_final_sec[deo_target] = 6
    data_final_sec['% School Observations by DEOs'] = data_final_sec['DEO']/data_final_sec[deo_target]
    data_final_sec[ceo_target] = 3
    data_final_sec['% School Observations by CEOs'] = data_final_sec['CEO']/data_final_sec[ceo_target]

    # Saving the report
    elem_report = report_utilities.get_elementary_report(data_final_elm, 'percent_ranking', ranking_args_dict, 'PPO', 'Palli Parvai')
    sec_report = report_utilities.get_secondary_report(data_final_sec, 'percent_ranking', ranking_args_dict, 'PPO', 'Palli Parvai')


    file_utilities.save_to_excel({'PPO_Elm': elem_report}, 'PPO_Elm.xlsx',\
             dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path())

    file_utilities.save_to_excel({'PPO_Sec': sec_report}, 'PPO_Sec.xlsx',\
             dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path())

if __name__ == "__main__":
    main()

