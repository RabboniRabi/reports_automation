"""
Module with utility functions that can be commonly used for different reports.
"""


import pandas as pd
#import reports_automation.ceo_reports.ranking as ranking
import os
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols

brc_file_name = 'BRC_CRC_Master_sheet.xlsx'
brc_master_sheet_name = 'BRC-CRC Updated sheet'

# Columns to be dropped from the BRC mapping sheet
brc_master_drop_cols = ['Cluster ID', 'CRC Udise','CRC School Name','BRTE']

# Define column names
beo_rank = 'BEO Rank'
deo_elem_rank = 'DEO (Elementary) Rank'
deo_sec_rank = 'DEO (Secondary) Rank'

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
deo_rank_elm = 'DEO Rank Elementary'
deo_rank_sec = 'DEO Rank Secondary'

# Define the list of columns to group by for rankings
beo_ranking_group_cols = [cols.district_name, beo_user, cols.beo_name]
deo_elem_ranking_group_cols = [cols.district_name, cols.deo_name_elm]
deo_secnd_ranking_group_cols = [cols.district_name, cols.deo_name_sec]


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
    report_summary = pd.merge(raw_data, brc_master_sheet,on=merge_dict['on_values'],how=merge_dict['how'])

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
    the BEO ranking, DEO(Elementary) ranking and updating the data.

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

    # If the data is at school level, filter the data to Elementary school type
    if (any(cols.elem_schl_lvl in col_name for col_name in df_summary.columns.to_list())):
        df_summary = df_summary[df_summary[school_level].isin([cols.elem_schl_lvl])]
        # Drop the school level column as it will no longer be needed
        df_summary.drop(columns=[cols.school_level],axis=1, inplace=True)                     

    # Get the ranking for the BEOs
    #beo_ranking = ranking_utilities.calc_ranking(df_summary, beo_ranking_group_cols, ranking_type, ranking_args_dict)

    # Make a copy of the ranking to update master sheet
    #beo_ranking_for_master = beo_ranking.copy()

    # Update the BEO ranked data with designation
    #beo_ranking_for_master[cols.desig] = 'BEO'

    # Rename the BEO name column
    #beo_ranking_for_master.rename(columns={cols.beo_name: cols.name, cols.district_name: cols.district}, inplace = True)

    #file_utilities.save_to_excel({'BEO Ranking': beo_ranking}, 'beo_ranking.xlsx')


    # Update the master ranking with the BEO ranking
    #ranking_utilities.update_ranking_master(beo_ranking_for_master, metric_code, metric_category, 'Elementary')

    deo_elm_ranking = ranking_utilities.calc_ranking(df_summary, deo_elem_ranking_group_cols, ranking_type, ranking_args_dict)

    #file_utilities.save_to_excel({'DEO Ranking': deo_elm_ranking}, 'deo_elem_ranking.xlsx')

    # Make a copy of the ranking to update master sheet
    deo_elm_ranking_for_master = deo_elm_ranking.copy()

    # Update the DEO ranked data with designation
    deo_elm_ranking_for_master[cols.desig] = 'DEO'

    # Rename the DEO name column
    deo_elm_ranking_for_master.rename(columns={cols.deo_name_elm: cols.name, cols.district_name: cols.district}, inplace = True)

    # Update the master ranking with the BEO ranking
    ranking_utilities.update_ranking_master(deo_elm_ranking_for_master, metric_code, metric_category, 'Elementary')

    # Merge the data with the ranks

    # Take only subset columns of BEO ranked data
    #beo_ranking = beo_ranking[[cols.beo_user, cols.beo_name, cols.rank_col, cols.ranking_value]]
    # Rename the rank column
    #beo_ranking.rename(columns={cols.rank_col: beo_rank}, inplace=True)

    # Take only subset columns of DEO ranked data
    deo_elm_ranking = deo_elm_ranking[[cols.deo_name_elm, cols.rank_col, cols.ranking_value]]
    # Rename the rank column
    deo_elm_ranking.rename(columns={cols.rank_col: deo_elem_rank}, inplace=True)

    # Since the ranking values will be grouped to beo level, the ranking values of each individual row
    # of data before being grouped and ranked is missed. That data will be more useful for review.
    # That data is inserted here. Not a clean way of doing things. Yes.
    ranking_args_dict['group_levels'] = ''
    data_level_ranking = ranking_utilities.calc_ranking(df_summary, deo_elem_ranking_group_cols, ranking_type, ranking_args_dict)


    #elementary_report = pd.merge(df_summary, beo_ranking, on=[cols.beo_user, cols.beo_name])
    #elementary_report = pd.merge(elementary_report, deo_elm_ranking, on=[cols.deo_name_elm])
    #elementary_report = pd.merge(elementary_report, data_level_ranking[[cols.deo_name_elm, cols.ranking_value]], on=[cols.deo_name_elm])

    # Replace the two lines below with the three lines above when beo ranking is enabled
    elementary_report = pd.merge(df_summary, deo_elm_ranking, on=[cols.deo_name_elm])
    elementary_report = pd.merge(elementary_report, data_level_ranking[[cols.deo_name_elm, cols.ranking_value]], on=[cols.deo_name_elm])

    # Sort the data by district and rank
    #elementary_report.sort_values(by=[deo_elem_rank, cols.deo_name_elm, beo_rank], ascending=True, inplace=True)
    # Replace the line above with the line below when beo ranking is done
    elementary_report.sort_values(by=[deo_elem_rank, cols.deo_name_elm], ascending=True, inplace=True)
    

    return elementary_report


def get_secondary_report(df_summary, ranking_type, ranking_args_dict, metric_code, metric_category):
    """
    Function create and return the secondary report on given data by calculating
    the DEO (Secondary) ranking and updating the data.

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

    # If the data is at school level, filter the data to Secondary school type
    if (any(cols.elem_schl_lvl in col_name for col_name in df_summary.columns.to_list())):
        df_summary = df_summary[df_summary[school_level].isin([scnd_schl_lvl])]
        # Drop the school level column as it will no longer be needed
        df_summary.drop(columns=[cols.school_level],axis=1, inplace=True)

    # Get the ranking for the secondary DEOs
    deo_sec_ranking = ranking_utilities.calc_ranking(df_summary, deo_secnd_ranking_group_cols, ranking_type, ranking_args_dict)

    # Make a copy of the ranking to update master sheet
    deo_sec_ranking_for_master = deo_sec_ranking.copy()

    # Update the DEO ranked data with designation
    deo_sec_ranking_for_master[cols.desig] = 'DEO'

    # Rename the DEO name column
    deo_sec_ranking_for_master.rename(columns={cols.deo_name_sec: cols.name, cols.district_name: cols.district}, inplace = True)

    file_utilities.save_to_excel({'DEO Ranking': deo_sec_ranking_for_master}, 'deo_sec_ranking_for_master.xlsx')

    # Update the master ranking with the DEOs ranking
    ranking_utilities.update_ranking_master(deo_sec_ranking_for_master, metric_code, metric_category, 'Secondary')

    #secondary_report = pd.append([report_summary, deo_sec_ranking], axis=1)

    # Take only subset columns of DEO ranked data
    deo_sec_ranking = deo_sec_ranking[[cols.deo_name_sec, cols.rank_col, cols.ranking_value]]
    # Rename the rank column
    deo_sec_ranking.rename(columns={cols.rank_col: deo_sec_rank}, inplace=True)

    # Since the ranking values will be grouped to DEO level, the ranking values of each individual row
    # of data before being grouped and ranked is missed. That data will be more useful for review.
    # That data is inserted here. Not a clean way of doing things. Yes.
    ranking_args_dict['group_levels'] = ''
    data_level_ranking = ranking_utilities.calc_ranking(df_summary, deo_secnd_ranking_group_cols, ranking_type, ranking_args_dict)

    secondary_report = pd.merge(df_summary, deo_sec_ranking, on=[cols.deo_name_sec])
    # Drop the DEO level ranking value
    secondary_report.drop(columns=[cols.ranking_value], axis = 1, inplace=True)
    # Add the data level ranking value
    #secondary_report[cols.ranking_value] = data_level_ranking[cols.ranking_value]
    secondary_report = pd.merge(secondary_report, data_level_ranking[[cols.deo_name_sec, cols.ranking_value]], on=[cols.deo_name_sec])

    # Sort the data by district and rank
    secondary_report.sort_values(by=[deo_sec_rank, cols.deo_name_sec], ascending=True, inplace=True)

    return secondary_report



