"""
Temporary script to calculate CEO ranking for all DEO level reports.
For each metric, the average ranks for all DEOS assigned to the CEO is calculated as the CEO rank.
"""


import sys
sys.path.append('../')

import math

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols

from enums.school_levels import SchoolLevels as school_levels
import readers.config_reader as config_reader

import pandas as pd

import ceo_deo_mapping as mapping

def calculate_ceo_ranks_for_deo_lvl_rpts():
    """
    Function to calculate the CEO ranks for DEO level reports.
    The function calculates the mean ranks of all DEOs assigned 
    to the CEO for each metric.

    Returns:
    -------
    Pands DataFrame object containing the ranks of all CEOs for all metrics
    """

    # Get the august ranking master
    dir_path = file_utilities.get_ceo_rpts_dir_path()
    file_path = file_utilities.get_file_path('ranking_master_july.xlsx', dir_path)

    df_ranking_master = file_utilities.read_sheet(file_path, sheet_name='ranking')

    # Get the list of unique metric codes
    metric_codes = df_ranking_master[cols.metric_code].unique().tolist()

    # Get the CEO DEO mapping
    ceo_deo_mapping = mapping.get_ceo_deo_mapping()

    df_ceo_ranking = pd.DataFrame()
    df_ceo_ranking['CEO'] = ceo_deo_mapping.keys()

    # Get the average rank of each CEO for each metric - not an efficient implementation below
    for metric_code in metric_codes:
        df_ceo_ranking[metric_code] = 0
        for ceo in ceo_deo_mapping.keys():
            # Get elementary DEOs
            elem_deos = ceo_deo_mapping[ceo]['Elementary_DEOs']
            sec_deos  = ceo_deo_mapping[ceo]['Secondary_DEOs']
            all_deos = elem_deos + sec_deos
            # Filter DEOs mapped to this CEO
            deos_of_ceo = utilities.filter_dataframe_column(df_ranking_master, cols.name, all_deos)
            
            # From that, filter dataframe for current metric_code
            deos_of_ceo_metric = utilities.filter_dataframe_column(deos_of_ceo, cols.metric_code, [metric_code])

            # Get the average rank of DEOs
            mean_ceo_rank_metric = round(deos_of_ceo_metric.loc[:,cols.rank_col].mean(),1)
            
            # Update rank of CEO for metric
            df_ceo_ranking[metric_code].loc[df_ceo_ranking['CEO']==ceo] = mean_ceo_rank_metric

    file_utilities.save_to_excel({'ceo_avg_rank': df_ceo_ranking}, 'ceo_ranks_for_deo_lvl_reports_july.xlsx', dir_path)        

    return df_ceo_ranking


def calculate_inverted_ceo_ranks_for_deo_lvl_rpts():
    """
    Function to calculate the inverted CEO ranks for each metric.
    For example, if the rank for a CEO for attendance metric was 7
    and max rank for the metric is 58, the inverted rank will be:
    58+1 - 7 = 52.

    The inverted rank values will be used to multiply with the weightage
    for a metric. So, higher the rank, (eg, 3/58), larger the inverted rank value (56),
    higher the score when multiplied with the weightage.

    """

    # Get the ranks of CEOs for all metrics
    df_ceo_ranking = calculate_ceo_ranks_for_deo_lvl_rpts()

    # Get metric wise maximum CEO rank possible
    metric_wise_max_ceo_rank_dict = get_metric_wise_ceo_max_rank()

    # For each metric, calculate the inverted rank
    for metric_code in metric_wise_max_ceo_rank_dict.keys():
        if metric_code in df_ceo_ranking.columns.to_list():
            max_rank = metric_wise_max_ceo_rank_dict[metric_code]
            df_ceo_ranking[metric_code] = (max_rank + 1) - df_ceo_ranking[metric_code]

    dir_path = file_utilities.get_ceo_rpts_dir_path()
    file_utilities.save_to_excel({'ceo_avg_inv_rank': df_ceo_ranking}, 'inverted_ceo_ranks_for_deo_lvl_reports_july.xlsx', dir_path)        




def get_schl_lvls_app_for_active_metrics():
    """
    Function to get the school levels applicability
    (elementary, secondary) for each of the active metrics in
    the ceo review configs

    Returns:
    --------
    Dictionary of metric code applicability.
    Eg: {
        'SCH_STU_ATT' : ['Elementary', 'Secondary'],
        'TRANS_5_6' : ['Elementary']
    }
    """

    # Get all the active configurations
    active_configs = config_reader.get_all_active_ceo_review_configs()

    # Define the metric-school levels applicability dictionary
    metric_schl_lvls_app = {}

    # For each of the configs
    for config in active_configs:
        # Get the metric code
        metric_code = config['report_code']

        schl_lvls = []
        # If generate report flag is true for Elementary configuration, add it to the school levels
        if config['elementary_report']['generate_report']:
            schl_lvls.append(school_levels.ELEMENTARY.value)

        # If generate report flag is true for Secondary configuraiton, add it to the school levels
        if config['secondary_report']['generate_report']:
            schl_lvls.append(school_levels.SECONDARY.value)

        metric_schl_lvls_app[metric_code] = schl_lvls

    return metric_schl_lvls_app



def get_metric_wise_ceo_max_rank():
    """
    Function to fetch the metric wise maximum possible rank for a CEO.
    This calculation is needed as metrics are applicable for either 
    Elementary (58 DEOs) only, Secondary (55 DEOs) only or both

    Returns:
    -------
    Dictionary of metric wise max possible rank
    """

    # Get number of elementary and secondary DEOs
    no_of_elem_deos = mapping.get_no_of_elem_deos()
    no_of_sec_deos = mapping.get_no_of_sec_deos()

    # Get the school levels applicability of metrics
    metric_schl_lvls_app = get_schl_lvls_app_for_active_metrics()

    metric_wise_rank = {}

    # For each metric, check the applicability of school levels
    # and assign the maximum possible rank

    for metric_code in metric_schl_lvls_app.keys():

        if school_levels.ELEMENTARY.value in metric_schl_lvls_app[metric_code] \
                    and school_levels.SECONDARY.value in metric_schl_lvls_app[metric_code] :
            max_rank = math.ceil((no_of_elem_deos + no_of_sec_deos)/2)
        elif school_levels.ELEMENTARY.value in metric_schl_lvls_app[metric_code]:
            max_rank = no_of_elem_deos
        elif school_levels.SECONDARY.value in metric_schl_lvls_app[metric_code]:
            max_rank = no_of_sec_deos

        metric_wise_rank[metric_code] = max_rank

    return metric_wise_rank
            



if __name__ == "__main__":
    calculate_inverted_ceo_ranks_for_deo_lvl_rpts()




