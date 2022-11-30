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

def concat_with_brc_master(raw_data,udise_col):
    """

    Parameters
    ----------
    raw_data

    Returns
    -------

    """

    brc_master_sheet = get_brc_master()
    brc_master_sheet = brc_master_sheet.drop(brc_master_drop_cols, axis=1)
    report_summary = pd.concat([raw_data,brc_master_sheet],keys=udise_col)
    print(report_summary.columns.to_list())

    return report_summary

def get_brc_master():
    """
    This function would return the master brc-crc file that would be required for merging with the raw data required
    in all other reports- CEO review or otherwise.

    """
    mapping_data_dir = file_utilities.get_mapping_data_dir_path()
    # read from excel, get sub columns
    brc_mapping_file_path = os.path.join(mapping_data_dir, brc_file_name)
    brc_master = pd.read_excel(brc_mapping_file_path,brc_master_sheet_name)
    return brc_master


def get_elementary_report(report_summary):

    """
    This module would return a dataframe with the list of entries that pertain to the elementary schools
    for any report that calls it.
    report_summary: The final dataframe that is returned after creating the specific report
    beo_ranking: this would be a column that has the BEO ranking for the specific report
    deo_elm_ranking: this would be a column that has the BEO ranking for the specific report
    """

    # Get the ranking for the BEOs
    beo_ranking = ranking_utilities.calc_ranking(df, ranking_type, ranking_args_dict)

    # Update the master ranking with the BEO ranking
    ranking_utilities.update_ranking_master(beo_ranking, metric_code, metric_category, 'Elementary')

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

    # Get the ranking for the secondary DEOs
    deo_sec_ranking = ranking_utilities.calc_ranking(df, ranking_type, ranking_args_dict)

    # Update the master ranking with the DEOs ranking
    ranking_utilities.update_ranking_master(deo_sec_ranking, metric_code, metric_category, 'Secondary')

    secondary_report = pd.append([report_summary, deo_sec_ranking], axis=1)

    return secondary_report


common_pool_basefile = file_utilities.user_sel_excel_filename()
raw_data = pd.read_excel(common_pool_basefile, sheet_name='Abstract')

udise_col = 'udise_code'

def main():
    df_test = concat_with_brc_master(raw_data,udise_col)
    print(df_test)
    return df_test



if __name__ == "__main__":
    main()


