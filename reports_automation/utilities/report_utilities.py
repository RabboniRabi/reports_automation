"""
Module with utility functions that can be commonly used for different reports.
"""


import pandas as pd
#import reports_automation.ceo_reports.ranking as ranking
import os
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities

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
beo_name = 'beo_name'
deo_user_elm = 'deo_name (elementary)'
deo_user_sec = 'deo_name (secondary)'
cwsn_students ='cwsn'
beo_rank = 'BEO Rank'
deo_rank_elm = 'DEO Rank Elementary'
deo_rank_sec = 'DEO Rank Secondary'

# Define the list of columns to group by for rankings
beo_ranking_group_cols = [district_name, beo_user, beo_name]
deo_elem_ranking_group_cols = [district_name, deo_user_elm]
deo_secnd_ranking_group_cols = [district_name, deo_user_sec]


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
    DataFrame object of the BRC-CRC mapping data
    """
    mapping_data_dir = file_utilities.get_mapping_data_dir_path()
    # read from excel, get sub columns
    brc_mapping_file_path = os.path.join(mapping_data_dir, brc_file_name)
    brc_master = pd.read_excel(brc_mapping_file_path,brc_master_sheet_name)
    return brc_master


def get_elementary_report(df_summary, ranking_type, ranking_args_dict, metric_code, metric_category):

    """
    Function create and return the elementary report on given data by calculating
    the BEO ranking, EO(Elementary) ranking and updating the data.

    The master ranking data is also updated when this function is called.

    Parameters: 
    -----------

    df_summary: Pandas DataFrame
        The raw processed, summarised and ready for ranking
    ranking_type: str
        The type of ranking to be used to calculate the ranking for the data
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_cols' : ['class_1', 'Total'],
        'agg_func' : 'sum',
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : True, 
        'ascending' : False
        }
    metric_code: str
        The code of the metric on which the data is ranked
    metric_category: str
        The category of the metric on which the data is ranked
    """

    # Filter the data to Elementary school type
    df_summary = df_summary[df_summary[school_level].isin(['Elementary School'])]

    file_utilities.save_to_excel({'Elementary shcools': df_summary}, 'Elementary_Schools.xlsx')

    print('df_summary filtered to elementary: ', df_summary)

    # Get the ranking for the BEOs
    beo_ranking = ranking_utilities.calc_ranking(df_summary, beo_ranking_group_cols, ranking_type, ranking_args_dict)

    print('beo_ranking', beo_ranking)

    file_utilities.save_to_excel({'BEO Ranking': beo_ranking}, 'beo_ranking.xlsx')

    # Update the master ranking with the BEO ranking
    """ranking_utilities.update_ranking_master(beo_ranking, metric_code, metric_category, 'Elementary')

    deo_elm_ranking = ranking.get_ranking(df, deo_user_elm, CP)

    elementary_report = pd.append([df_summary,beo_ranking,deo_elm_ranking], axis=1)

    return elementary_report"""


def get_secondary_report(report_summary):
    """
    Function create and return the elementary report on given data by calculating
    the BEO ranking, DEO(Secondary) ranking and updating the data.

    The master ranking data is also updated when this function is called.

    Parameters: 
    -----------

    df_summary: Pandas DataFrame
        The raw processed, summarised and ready for ranking
    ranking_type: str
        The type of ranking to be used to calculate the ranking for the data
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_cols' : ['class_1', 'Total'],
        'agg_func' : 'sum',
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : True, 
        'ascending' : False
        }
    metric_code: str
        The code of the metric on which the data is ranked
    metric_category: str
        The category of the metric on which the data is ranked
    """

    # Filter the data to Secondary school type
    df_summary = df_summary[df_summary[school_level].isin('Secondary')]

    # Get the ranking for the secondary DEOs
    deo_sec_ranking = ranking_utilities.calc_ranking(df, ranking_type, ranking_args_dict)

    # Update the master ranking with the DEOs ranking
    ranking_utilities.update_ranking_master(deo_sec_ranking, metric_code, metric_category, 'Secondary')

    secondary_report = pd.append([report_summary, deo_sec_ranking], axis=1)

    return secondary_report



