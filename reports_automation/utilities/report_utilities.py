"""
Module with utility functions that can be commonly used for different reports.
"""


import pandas as pd
#import reports_automation.ceo_reports.ranking as ranking
import os
import utilities.file_utilities as file_utilities

brc_file_name = 'BRC_CRC_Master_sheet.xlsx'
brc_master_sheet_name = 'BRC-CRC Updated sheet'

# Columns to be dropped from the BRC mapping sheet
brc_master_drop_cols = ['Cluster ID', 'CRC Udise','CRC School Name']

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
deo_user_elm = 'deo_name (elementary)'
deo_user_sec = 'deo_name (secondary)'
cwsn_students ='cwsn'
beo_rank = 'BEO Rank'
deo_rank_elm = 'DEO Rank Elementary'
deo_rank_sec = 'DEO Rank Secondary'

def map_data_with_brc(raw_data, merge_dict):
    """
    Function to map the raw data with BRC CRC mapping. The join is done on
    school UDISE values.

    Parameters
    ----------
    raw_data: Pandas DataFrame
        The raw data to be updated with brc-crc mapping
    merge_dict: dict
        A merge param - merge param value key-value pair to be used to specify the type of merging
        Eg: merge_dict = {
            'on_values' : ['district', 'block','school_name', 'school_category', 'udise_col'],
            'how' : 'outer'
        }

    Returns
    -------
    DataFrame object of given data updated with BRc-CRC mapping
    """

    brc_master_sheet = get_brc_master()
    brc_master_sheet = brc_master_sheet.drop(brc_master_drop_cols, axis=1)
    report_summary = pd.merge(brc_master_sheet,raw_data,on=merge_dict['on_values'],how=merge_dict['how'])

    return report_summary

def get_brc_master():
    """
    This function would return the master brc-crc file that would be required for merging with the raw data required
    in all other reports- CEO review or otherwise.

    Returns:
    -------
    DataFrame object of the BRC-CRC mapping data0

    """
    mapping_data_dir = file_utilities.get_mapping_data_dir_path()
    # read from excel, get sub columns
    brc_mapping_file_path = os.path.join(mapping_data_dir, brc_file_name)
    brc_master = pd.read_excel(brc_mapping_file_path,brc_master_sheet_name)
    return brc_master


def get_elementary_report(report_summary):

    """
    This function creates the elementary report on given data by calculating
    the BEO ranking and DEO(Elementary) ranking.

    - Method to be updated post integration with ranking functionality.

    report_summary: The final dataframe that is returned after creating the specific report
    beo_ranking: this would be a column that has the BEO ranking for the specific report
    deo_elm_ranking: this would be a column that has the BEO ranking for the specific report
    """

    beo_ranking = ranking.get_ranking(df,beo_user,CP)
    deo_elm_ranking = ranking.get_ranking(df, deo_user_elm, CP)

    elementary_report = pd.append([report_summary,beo_ranking,deo_elm_ranking], axis=1)

    return elementary_report


def get_secondary_report(report_summary):
    """
    This module would return a dataframe with the list of entries that pertain to the secondary schools
    for any report that calls it.
    report_summary: The final dataframe that is returned after creating the specific report
    deo_sec_ranking: this would be a column that has the BEO ranking for the specific report
    """

    deo_sec_ranking = ranking.get_ranking(df, deo_user_sec, CP)

    secondary_report = pd.append([report_summary, deo_sec_ranking], axis=1)

    return secondary_report



