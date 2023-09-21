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

    # Get the current month data 
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


    # Get the previous month data
    prev_month = utilities.get_prev_month()
    prev_month_year = utilities.get_year_of_prev_month()
    df_prev_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [prev_month], [int(prev_month_year)])

    
    # Get the data in progress report format
    df_prev_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_prev_month_ranks)

    # Get the improvement report - Difference in metric ranks in current month from previous month
    df_improv = utilities.subtract_dfs(df_curr_month_rpt, df_prev_month_rpt, curr_month_metric_codes)

    # Get the metric wise improvement weightages
    metric_improv_weightages = weightage_fetcher.fetch_ceo_rev_metric_improv_weightages(deo_lvl.value)

    # Get the improvement consolidated ranking
    df_improv_cons_ranking = ranking_utilities.compute_consolidated_ranking(df_improv, \
                                            metric_improv_weightages, invert_rank=False)

    # Compute the overall ranking
    df_overall_ranking = pd.DataFrame()
    df_overall_ranking[cols.name] = df_curr_month_rpt[cols.name]
    df_overall_ranking['Current month weighted Score'] = curr_month_cons_ranking['Total Weighted Score']
    df_overall_ranking['Improvement weighted Score'] = df_improv_cons_ranking['Total Weighted Score']
    df_overall_ranking['Overall Weighted Score'] = df_overall_ranking['Current month weighted Score'] + \
                                                        df_overall_ranking['Improvement weighted Score']    

    # Sort the values and rank
    df_overall_ranking = df_overall_ranking.sort_values(by='Overall Weighted Score', \
                                    ascending=False).reset_index()

    df_overall_ranking[cols.rank_col] = df_overall_ranking['Overall Weighted Score']\
                                                    .rank(ascending=False, method='min')

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

    


