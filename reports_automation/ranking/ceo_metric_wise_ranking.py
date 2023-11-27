"""
Temporary script to calculate CEO ranking for all DEO level reports.
For each metric, the average ranks for all DEOS assigned to the CEO is calculated as the CEO rank.
"""


import sys
sys.path.append('../')

import math
import warnings

warnings.filterwarnings('ignore')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols

from enums.school_levels import SchoolLevels as school_levels
import readers.config_reader as config_reader
import readers.weightage_fetcher as weightage_fetcher

import pandas as pd

import miscellaneous.ceo_deo_mapping as mapping

# Get the current month data
curr_month = utilities.get_curr_month()
curr_year = utilities.get_curr_year()
dir_path = file_utilities.get_ranking_reports_dir()
def calculate_weighted_score_for_ceo_rank_rpts(df_ceo_ranking):
    """
    Function to calculate the score based on the metric weightage
    Parameters:
    -------
        df_ceo_ranking: Dataframe with the inverted ranks

    Returns:
    -------
    CEO Level weighted score dataframe
    """
    # Getting the metric weightage for the active configs
    metric_weightages = weightage_fetcher.fetch_ceo_rev_metric_ranking_weightages()
    # Extracting metrics that have weightages
    weighted_metrics = {metric: metric_weightages[metric] for metric in metric_weightages.keys() if metric_weightages[metric] != 0}
    # Loop to iterate for each metric code
    for metric_code in weighted_metrics.keys():
        # Multiplying that column with the weightage
        df_ceo_ranking[metric_code] = df_ceo_ranking[metric_code] * metric_weightages[metric_code]

    # Sorting the dataframe by districts
    df_ceo_ranking.sort_values(by="CEO", inplace=True)
    # Adding a key-value pair for adding weightage column in the dataframe
    weighted_metrics["CEO"] = "Weightage"
    df_ceo_ranking.loc[len(df_ceo_ranking)] = weighted_metrics

    return df_ceo_ranking
def calculate_ceo_ranks_for_deo_lvl_rpts():
    """
    Function to calculate the CEO ranks for DEO level reports.
    The function inverts the ranks and then calculates the mean ranks of all DEOs assigned
    to the CEO for each metric.

    Returns:
    -------
    Pands DataFrame object containing the ranks of all CEOs for all metrics
    """

    # Get the august ranking master

    metric_schl_lvls_app = get_schl_lvls_app_for_active_metrics()

    df_ranking_master = ranking_utilities.get_ceo_rev_ranking_master_data(['DEO'], \
                    [school_levels.ELEMENTARY.value, school_levels.SECONDARY.value], \
                    [curr_month], [int(curr_year)])
                                
    # Get the list of unique metric codes
    metric_codes  = df_ranking_master[cols.metric_code].unique()

    # Get the CEO DEO mapping
    ceo_deo_mapping = mapping.get_ceo_deo_mapping()


    df_ceo_ranking = pd.DataFrame()
    df_ceo_ranking['CEO'] = ceo_deo_mapping.keys()
    no_of_elem_deos = mapping.get_no_of_elem_deos()
    no_of_sec_deos = mapping.get_no_of_sec_deos()

    metric_weightages = weightage_fetcher.fetch_ceo_rev_metric_ranking_weightages()

    # Get the average rank of each CEO for each metric - not an efficient implementation below
    for metric_code in metric_codes:
        
        # If weightage for metric code is 0, skip the metric code
        if metric_weightages[metric_code] == 0:
            continue

        df_ceo_ranking[metric_code] = 0
        for ceo in ceo_deo_mapping.keys():
            # Get elementary DEOs
            elem_deos = ceo_deo_mapping[ceo]['Elementary_DEOs']
            sec_deos = ceo_deo_mapping[ceo]['Secondary_DEOs']
            all_deos = elem_deos + sec_deos
            # Filter DEOs mapped to this CEO
            deos_of_ceo = utilities.filter_dataframe_column(df_ranking_master, cols.name, all_deos)
            
            # From that, filter dataframe for current metric_code
            deos_of_ceo_metric = utilities.filter_dataframe_column(deos_of_ceo, cols.metric_code, [metric_code])

            sec_df = deos_of_ceo_metric[deos_of_ceo_metric[cols.school_level] == "Secondary"]

            sec_df[cols.rank_col] = (no_of_sec_deos + 1) - sec_df[cols.rank_col]
            metric_code_sch_lvl_list = metric_schl_lvls_app[metric_code]
            if len(metric_code_sch_lvl_list) == 2:
                # Filtering for Elementary
                elem_df = deos_of_ceo_metric[deos_of_ceo_metric[cols.school_level] == "Elementary"]
                # Inverting the ranks - 1st rank becomes 58 for weightage multiplication
                elem_df[cols.rank_col] = (no_of_elem_deos + 1) - elem_df[cols.rank_col]
                # Getting the average for the respective Elementary DEO
                elem_rank_avg = (elem_df[cols.rank_col].mean()) / no_of_elem_deos
                # Filtering for Secondary
                sec_df = deos_of_ceo_metric[deos_of_ceo_metric[cols.school_level] == "Secondary"]
                # Inverting the ranks for secondary
                sec_df[cols.rank_col] = (no_of_sec_deos + 1) - sec_df[cols.rank_col]
                # Getting the average for the respective Secondary DEO
                sec_rank_avg = (sec_df[cols.rank_col].mean()) / no_of_sec_deos
                # Adding both the Average ranks and dividing it by 2
                ceo_rank = (elem_rank_avg + sec_rank_avg)/2
                mean_ceo_rank = round(ceo_rank, 2)
            elif len(metric_code_sch_lvl_list) == 1 and metric_code_sch_lvl_list[0] == "Elementary":
                # Filtering for Elementary
                elem_df = deos_of_ceo_metric[deos_of_ceo_metric[cols.school_level] == "Elementary"]
                # Inverting the ranks
                elem_df[cols.rank_col] = (no_of_elem_deos + 1) - elem_df[cols.rank_col]
                # If there is only one school level report for a particular metric then no need to divide it by 2
                elem_rank_avg = (elem_df[cols.rank_col].mean()) / no_of_elem_deos
                mean_ceo_rank = round(elem_rank_avg, 2)
            else:
                # Filtering for Secondary
                sec_df = deos_of_ceo_metric[deos_of_ceo_metric[cols.school_level] == "Secondary"]
                # Inverting the ranks for secondary
                sec_df[cols.rank_col] = (no_of_sec_deos + 1) - sec_df[cols.rank_col]
                # Getting the average for the respective Secondary DEO
                sec_rank_avg = (sec_df[cols.rank_col].mean()) / no_of_sec_deos
                mean_ceo_rank = round(sec_rank_avg, 2)
            # Update rank of CEO for metric
            df_ceo_ranking[metric_code].loc[df_ceo_ranking['CEO'] == ceo] = mean_ceo_rank
    # Replacing null values to 0
    df_ceo_ranking.fillna(0, inplace=True)

    return df_ceo_ranking

def get_ceo_cons_ranking_deo_lvl_rpts():
    """
    Function to get CEO consolidated ranking with their weighted scores and saving it as excel file

    """
    # Get the CEO consolidating report
    ceo_cons_df = calculate_ceo_ranks_for_deo_lvl_rpts()
    # Get the weighted score report
    weighted_score_df = calculate_weighted_score_for_ceo_rank_rpts(ceo_cons_df.copy())

    # Saving the file
    file_utilities.save_to_excel({'ceo_avg_rank': ceo_cons_df},
                                 'ceo_ranks_for_deo_lvl_reports_' + str(curr_month).lower() + '.xlsx', dir_path)
    file_utilities.save_to_excel({'ceo_avg_rank': weighted_score_df},
                                 'ceo_ranks_weighted_score_' + str(curr_month).lower() + '.xlsx', dir_path)





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



if __name__ == "__main__":
    get_ceo_cons_ranking_deo_lvl_rpts()




