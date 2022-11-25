"""
Module with utility functions that can be commonly used for different reports.
"""


import pandas as pd
import reports_automation.ceo_reports.ranking as ranking

def report_summary(raw_data,brc_master_sheet,district_name,deo_user_elm,deo_user_sec,block_name,beo_user,udise_col,
                        school_category,school_level):

    report_summary = pd.concat([brc_master_sheet[district_name,deo_user_elm,deo_user_sec,block_name,beo_user,udise_col,
                        school_category,school_level],raw_data], axis=1)

    return report_summary

def get_elementary_report(report_summary):

    """
    This module would return a dataframe with the list of entries that pertain to the elementary schools
    for any report that calls it.
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
    deo_elm_ranking: this would be a column that has the BEO ranking for the specific report
    """

    deo_sec_ranking = ranking.get_ranking(df, deo_user_sec, CP)

    secondary_report = pd.append([report_summary, deo_sec_ranking], axis=1)

    return secondary_report








