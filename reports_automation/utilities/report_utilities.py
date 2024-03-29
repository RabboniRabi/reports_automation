"""
Module with utility functions that can be commonly used for different reports.
"""

import pandas as pd
#import reports_automation.ceo_reports.ranking as ranking
import os
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols

from enums.combine_data_types import CombineDataTypes as combine_data_types

brc_file_name = 'BRC_CRC_Master_V3.xlsx'
brc_master_sheet_name = 'BRC-CRC V1'

# Columns to be dropped from the BRC mapping sheet
brc_master_drop_cols = ['CRC Udise','CRC School Name']#, 'BRTE'

# Define the list of columns to group by for rankings
beo_ranking_group_cols = [cols.beo_user, cols.beo_name]
deo_elem_ranking_group_cols = [cols.deo_name_elm]
deo_secnd_ranking_group_cols = [cols.deo_name_sec]


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
    report_summary = pd.merge(raw_data, brc_master_sheet,on=merge_dict['join_on'],how=merge_dict['merge_type'])
    
    # Rearrage the columns so that DEO and BEO information comes at the begining of the data
    # Define rearranged order of columns
    list_of_cols = [cols.district_name] + [cols.deo_name_sec, cols.deo_name_elm, cols.beo_user, cols.beo_name, cols.school_level, cols.school_category]\
                     +  raw_data.columns.to_list()

    # Get the unique list of columns in the same order
    list_of_cols = pd.unique(pd.Series(list_of_cols)).tolist()

    report_summary = report_summary.reindex(columns=list_of_cols)

    return report_summary

def get_brc_master(sheet_name=brc_master_sheet_name):
    """
    This function would return the master brc-crc file that would be required for merging with the raw data required
    in all other reports- CEO review or otherwise.
    sheet_name: str
        Name of the sheet to read from BRC Master. Default is brc_master_sheet_name.

    Returns:
    -------
    DataFrame object of the BRC-CRC mapping data
    """
    mapping_data_dir = file_utilities.get_mapping_data_dir_path()
    # read from excel, get sub columns
    brc_mapping_file_path = os.path.join(mapping_data_dir, brc_file_name)
    brc_master = pd.read_excel(brc_mapping_file_path,sheet_name=sheet_name)

    return brc_master


def get_elem_ranked_report(df_summary, ranking_config, metric_code, metric_category):

    """
    Function create and return the elementary ranked report on given data by calculating
    the DEO(Elementary) ranking and updating the data.

    The master ranking data is also updated when this function is called.

    Parameters: 
    -----------

    df_summary: Pandas DataFrame
        The raw processed, summarised and ready for ranking
    ranking_config: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg:
            'ranking_config' : {
                'ranking_args': {
                    'ranking_type' : 'percent_ranking',
                    'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
                    'ranking_val_desc' : '% moved to CP',
                    'num_col' : 'class_1',
                    'den_col' : 'Total',
                    'sort' : true,
                    'ascending' : false,
                    '// Below configs are to be used' : '//if data is to be ranked directly without grouping',
                    '// Below configs are ignored' :  '//if data_ranking_levels config is present',
                    'show_rank_col' : true/false,
                    'rank_col_name' : 'to be given if show_rank_col is true',
                    'show_rank_val: : true/false,
                    'ranking_val_desc' : 'to be given if show_rank_val is true'
                }
                '//Below data ranking levels are optional' : '//To be used if data is to be grouped and ranked'
                'data_ranking_levels' : {
                    'deo_level' : {
                        'grouping_levels' : ['cols.deo_name'],
                        'show_rank_col' : true,
                        'rank_col_name' : 'cols.deo_elem_rank',
                        'show_rank_val' : false,
                        '//ranking_val_desc is not needed' : '//as show_rank_val flag is false
                    },
                    'block_level' : {
                        'grouping_levels' : ['cols.deo_name', 'cols.block_name'],
                        'show_rank_col': false,
                        '//rank_col_name is not needed' : '//as show_rank_col flag is false
                        'show_rank_val' : true,
                        'ranking_val_desc' : 'cols.perc_screened'
                    }
                }
            } 
    metric_code: str
        The code of the metric on which the data is ranked
    metric_category: str
        The category of the metric on which the data is ranked
    """

    # If the data is at school level, filter the data to Elementary school type
    if (any(cols.school_level in col_name for col_name in df_summary.columns.to_list())):
        df_summary = df_summary[df_summary[cols.school_level].isin([cols.elem_schl_lvl])]
        # Drop the school level column as it will no longer be needed
        df_summary.drop(columns=[cols.school_level],axis=1, inplace=True)                     

    # Get Elementary report, ranked
    elem_ranked_report = ranking_utilities.calc_ranking(df_summary, ranking_config)

    # Update the master ranking with the DEO ranking
    ranking_utilities.update_deo_ranking_master(df_summary, ranking_config, metric_code, metric_category, 'Elementary')

    # Sort the data by DEO Ranks
    elem_ranked_report.sort_values(by=[cols.deo_elem_rank, cols.deo_name_elm], ascending=True, inplace=True)

    # Drop duplicate columns
    elem_ranked_report = elem_ranked_report.T.drop_duplicates().T


    return elem_ranked_report


def get_sec_ranked_report(df_summary, ranking_config, metric_code, metric_category):
    """
    Function create and return the ranked secondary report on given data by calculating
    the DEO (Secondary) ranking and updating the data.

    The master ranking data is also updated when this function is called.

    Parameters: 
    -----------

    df_summary: Pandas DataFrame
        The raw processed, summarised and ready for ranking
    ranking_config: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg:
            'ranking_config' : {
                'ranking_args': {
                    'ranking_type' : 'percent_ranking',
                    'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
                    'ranking_val_desc' : '% moved to CP',
                    'num_col' : 'class_1',
                    'den_col' : 'Total',
                    'sort' : true,
                    'ascending' : false,
                    '// Below configs are to be used' : '//if data is to be ranked directly without grouping',
                    '// Below configs are ignored' :  '//if data_ranking_levels config is present',
                    'show_rank_col' : true/false,
                    'rank_col_name' : 'to be given if show_rank_col is true',
                    'show_rank_val: : true/false,
                    'ranking_val_desc' : 'to be given if show_rank_val is true'
                }
                '//Below data ranking levels are optional' : '//To be used if data is to be grouped and ranked'
                'data_ranking_levels' : {
                    'deo_level' : {
                        'grouping_levels' : ['cols.deo_name'],
                        'show_rank_col' : true,
                        'rank_col_name' : 'cols.deo_elem_rank',
                        'show_rank_val' : false,
                        '//ranking_val_desc is not needed' : '//as show_rank_val flag is false
                    },
                    'block_level' : {
                        'grouping_levels' : ['cols.deo_name', 'cols.block_name'],
                        'show_rank_col': false,
                        '//rank_col_name is not needed' : '//as show_rank_col flag is false
                        'show_rank_val' : true,
                        'ranking_val_desc' : 'cols.perc_screened'
                    }
                }
            } 
    metric_code: str
        The code of the metric on which the data is ranked
    metric_category: str
        The category of the metric on which the data is ranked
    """

    # If the data is at school level, filter the data to Secondary school type
    if (any(cols.school_level in col_name for col_name in df_summary.columns.to_list())):
        df_summary = df_summary[df_summary[cols.school_level].isin([cols.scnd_schl_lvl])]
        # Drop the school level column as it will no longer be needed
        df_summary.drop(columns=[cols.school_level], inplace=True)

    # Get secondary report, ranked
    sec_ranked_report = ranking_utilities.calc_ranking(df_summary, ranking_config)

    # Update the master ranking with the DEO ranking
    ranking_utilities.update_deo_ranking_master(df_summary, ranking_config, metric_code, metric_category, 'Secondary')

    # Sort the data by DEO rank
    sec_ranked_report.sort_values(by=[cols.deo_sec_rank, cols.deo_name_sec], ascending=True, inplace=True)

    # Drop duplicate columns
    sec_ranked_report = sec_ranked_report.T.drop_duplicates().T

    return sec_ranked_report



def combine_multiple_datasets(df_data_set:dict, combine_type:str, combine_data_configs:dict):
    """ 
    Function to combine multiple datasets into a single data frame object.

    Parameters:
    -----------
    df_data_set: dict
        Dictionary of datasets with the keys being the name of the data and value being the data
    combine_data_configs: dict
        Dictionary of configurations to combine the data on 

    Returns: Pandas DataFrame
        The combined data as a single dataframe object
    """

    if combine_type == combine_data_types.MERGE.value:
        # Merge the data

        # Get the primary data to which the rest of the data sets need to be merged
        primary_merge_data_config = combine_data_configs['primary_merge_data'] 
        primary_merge_data_name = primary_merge_data_config['source_name']

        # Drop and assign the primary data set to a variable that will hold the overall combined data
        cols_to_drop = primary_merge_data_config['cols_to_drop_before_merge'] 
        df_combined = df_data_set[primary_merge_data_name].drop(columns=cols_to_drop)

        # Delete the primary data reference from the config dictionary as the 
        # dictionary keys will be iterated in the next step - not a clean way of doing things
        del combine_data_configs['primary_merge_data']


        for key in combine_data_configs.keys():
            # Get the merge config
            merge_config = combine_data_configs[key]
            # Get the data for the key in merge config, drop any columns to be dropped and then merge
            df_data = df_data_set[key].drop(columns=merge_config['cols_to_drop_before_merge'])
            df_combined = df_combined.merge(df_data, how=merge_config['merge_type'], on=merge_config['join_on'])

    elif combine_type == combine_data_types.CONCAT.value:
        # Concatenate the data

        # Initially set the merged data to empty dataframe object
        df_combined = pd.DataFrame()
        for key in combine_data_configs.keys():
            # Get the concatenation config
            concat_config = combine_data_configs[key]
            # Get the data for the key in concat, drop any columns to be dropped config and then concatenate
            if 'cols_to_drop_before_concat' in concat_config:
                df_data = df_data_set[key].drop(columns=concat_config['cols_to_drop_before_concat'])
            else:
                df_data = df_data_set[key]
            df_combined = pd.concat([df_combined, df_data], join=concat_config['join']) 

    return df_combined

