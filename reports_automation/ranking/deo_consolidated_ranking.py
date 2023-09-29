"""
Module with functions to generate consolidated ranking for DEOs
based on ranks for metric based reports generated for CEO review.
"""

import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import readers.weightage_fetcher as weightage_fetcher

import utilities.column_names_utilities as cols

import pandas as pd


from enums.school_levels import SchoolLevels as school_levels

def generate_ceo_rev_deo_cons_ranking(deo_lvl: school_levels):
    """
    Function to generate the consolidated ranking for DEOs (Elementary/Secondary)
    based on the ranks for the metric based reports generated 
    for the monthly CEO review.

    Parameters:
    ----------
    deo_lvl:school_levels
        school_levels enum value indicating if report needs to be generated for 
        Elementary or Secondary DEOs
    """

    # Get the current month ranks for DEOs
    curr_month = utilities.get_curr_month()
    curr_year = utilities.get_curr_year()
    df_curr_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [curr_month], [int(curr_year)])
                                
    curr_month_metric_codes  = df_curr_month_ranks[cols.metric_code].unique()

    # Get the data in progress report format
    df_curr_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_curr_month_ranks)

    # Get the metric wise ranking weightages
    metric_ranking_weightages = weightage_fetcher.fetch_ceo_rev_metric_ranking_weightages(deo_lvl.value)

    # Get the current month consolidated ranking
    curr_month_cons_ranking = ranking_utilities.compute_consolidated_ranking(df_curr_month_rpt, \
                                            metric_ranking_weightages)

    # Get the previous month ranks for DEOs
    prev_month = utilities.get_prev_month()
    prev_month_year = utilities.get_year_of_prev_month()
    df_prev_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [prev_month], [int(prev_month_year)])

    # Get the data in progress report format
    df_prev_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_prev_month_ranks)

    # Get the improvement report - Difference in metric ranks in current month from previous month
    df_improv = utilities.subtract_dfs(df_prev_month_rpt, df_curr_month_rpt , curr_month_metric_codes, cols.name)

    # Remove negative values due to drop in ranking. Only improvement in ranking to be taken into account
    df_improv = df_improv.applymap(utilities.replace_negatives)

    # Get the metric wise improvement weightages
    metric_improv_weightages = weightage_fetcher.fetch_ceo_rev_metric_improv_weightages(deo_lvl.value)

    # Get the improvement consolidated ranking
    df_improv_cons_ranking = ranking_utilities.compute_consolidated_ranking(df_improv, \
                                            metric_improv_weightages, invert_rank=False)
    
    # Rename the total weighted score column name
    df_improv_cons_ranking.rename(columns={cols.cons_tot_wt_scr:cols.cons_impr_wt_scr}, inplace=True)

    # Compute the overall ranking (sum of consolidated weight + improvement weight)
    df_overall_ranking = curr_month_cons_ranking.copy()
    
    # Trim the data to name and current month weighted score column
    df_overall_ranking = df_overall_ranking[[cols.name, cols.cons_tot_wt_scr]]
    df_overall_ranking.rename(columns={cols.cons_tot_wt_scr:cols.cons_curr_wt_scr}, inplace=True)
    
    # Merge the improvement scores
    df_overall_ranking = df_overall_ranking.merge(df_improv_cons_ranking[[cols.name, cols.cons_impr_wt_scr]],
                                                    how='left', on=[cols.name])

    # Add the current month consolidated weight and improvement weight
    df_overall_ranking[cols.cons_ovr_wt_scr] = df_overall_ranking[cols.cons_curr_wt_scr] + \
                                                        df_overall_ranking[cols.cons_impr_wt_scr]  

    # Sort the values and rank
    df_overall_ranking = df_overall_ranking.sort_values(by=cols.cons_ovr_wt_scr, \
                                    ascending=False)

    df_overall_ranking[cols.rank_col] = df_overall_ranking[cols.cons_ovr_wt_scr]\
                                                    .rank(ascending=False, method='min')

    # Get the file name to save the DEOs overall ranking
    dir_path = file_utilities.get_cons_ranking_reports_dir()
    file_name = 'DEO_' + deo_lvl.value + '_' + curr_month + '_consolidated_ranking.xlsx'

    # Put the overall ranking, current month ranking and improvement ranking in three sheets
    df_dict = {
        'Overall': df_overall_ranking,
        'Current Month' : curr_month_cons_ranking,
        'Improvement' : df_improv_cons_ranking
        }

    # Save the data
    file_utilities.save_to_excel(df_dict, file_name, dir_path)




if __name__ == '__main__':

    # Generate the elementary DEOs overall ranking report
    generate_ceo_rev_deo_cons_ranking(school_levels.ELEMENTARY)

    # Generate the secondary DEOs overall ranking report
    generate_ceo_rev_deo_cons_ranking(school_levels.SECONDARY)

    


