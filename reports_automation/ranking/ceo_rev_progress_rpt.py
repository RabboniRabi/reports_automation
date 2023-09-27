"""
Module with functions to generate progress reports with visual
indicators to highlight improvement/decrease in performance between
current and previous reports
"""

import sys
sys.path.append('../')

import numpy as np

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.format_utilities as format_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.weightage_fetcher as weightage_fetcher

from enums.school_levels import SchoolLevels as school_levels


def generate_ceo_rev_deo_progress_report(deo_lvl: school_levels):
    """
    Function to generate a progress report for DEOs
    based on improvement/drop in ranks for each metric compared
    between current month and previous month.

    Parameters:
    -----------
    deo_lvl:school_levels
        school_levels enum value indicating if report needs to be generated for 
        Elementary or Secondary DEOs

    """

    # Get the current month data 
    curr_month = utilities.get_curr_month()
    curr_year = utilities.get_curr_year()
    df_curr_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [curr_month], [int(curr_year)])

    # Get the ranked metrics for current month                    
    curr_month_metric_codes  = df_curr_month_ranks[cols.metric_code].unique()

    # Filter out the metrics with zero weightage for the month
    metric_weightage_dict = weightage_fetcher.fetch_ceo_rev_metric_ranking_weightages(deo_lvl)
    metrics_to_omit = []
    for metric_code in curr_month_metric_codes:
        if metric_weightage_dict[metric_code] == 0:
            metrics_to_omit.append(metric_code)

    # Get the metrics with non zero weightage
    non_zero_wt_metrics = list(filter(lambda i : i not in metrics_to_omit, curr_month_metric_codes))

    # Filter the current month ranking data to only ranks with weightage
    df_curr_month_ranks = utilities.filter_dataframe_column(df_curr_month_ranks, cols.metric_code, non_zero_wt_metrics)


    # Get the data in progress report format
    df_curr_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_curr_month_ranks)

    # Get the previous month data
    prev_month = utilities.get_prev_month()
    prev_month_year = utilities.get_year_of_prev_month()
    df_prev_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [prev_month], [int(prev_month_year)])

    # Filter only rank data for the non zero weighted metrics used in the current month
    df_prev_month_ranks = utilities.filter_dataframe_column(df_prev_month_ranks, cols.metric_code, non_zero_wt_metrics)
    
    
    # Get the data in progress report format
    df_prev_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_prev_month_ranks)

    metric_code_append_txt = ' improvement'


    # Get the improvement report - Difference in metric ranks in current month from previous month
    df_improv = utilities.subtract_dfs(df_prev_month_rpt, df_curr_month_rpt , non_zero_wt_metrics, cols.name)

    # Append 'improvement' text to the metric code column names before merging it with the current month report
    rename_dict = {}
    for metric_code in non_zero_wt_metrics:
        rename_dict[metric_code] = metric_code + metric_code_append_txt
    df_improv.rename(columns=rename_dict, inplace=True)

    # Merge the rank improvement values data with the current month ranks
    df_curr_month_progress_rpt = df_curr_month_rpt.merge(df_improv, how='left', on=[cols.name])


    # Reorder the metric codes and their corresponding improvement columns together
    df_curr_month_progress_rpt = _reorder_progress_report_cols(df_curr_month_progress_rpt, \
                                    non_zero_wt_metrics, metric_code_append_txt)

    # Sort the data by DEO name
    df_curr_month_progress_rpt.sort_values(by=cols.name, inplace=True)
    
    """Format the report to visually highlight improvements"""

    dir_path = file_utilities.get_progress_reports_dir()

    # Get the xlsxwriter object of the data to be formatted and saved
    writer = file_utilities.get_xlsxwriter_obj({deo_lvl.value:df_curr_month_progress_rpt}, \
                       'DEO_' +  deo_lvl.value + '_' + curr_month +  '_progress_rpt.xlsx', dir_path)

    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name(deo_lvl.value)

    # Get the column names of the metrics' improvement
    metric_codes_improv_names = [f'{x}'+ metric_code_append_txt for x in non_zero_wt_metrics]


    # Get the format configs
    progress_rpt_format_configs = config_reader.get_misc_rpt_config('CEO_REV_PRG_RPT_FRMT')
    format_dicts_list = progress_rpt_format_configs['format_dicts_list']

    # Update the columns in the format_dicts_list
    for format_dict in format_dicts_list:
        format_dict['columns'] = metric_codes_improv_names

    # Apply the formatting
    format_utilities.apply_formatting(format_dicts_list, df_curr_month_progress_rpt, worksheet, workbook, start_row=1)
    
    writer.save()




def _reorder_progress_report_cols(df_progress_rpt, metric_codes:list, metric_code_append_txt: str):
    """
    Internal helper function to reorder the metric code columns and their corresponding improvement
    values column together for easy readability

    Parameters:
    -----------
    df_progress_rpt: Pandas DataFrame
        The progress report whose metric code columns are to be rearranged
    metric_codes: list
        The list of metric codes in the progress report
    metric_code_append_txt: str
        The text appended to the improvement metric code columns
    
    Returns:
    --------
    Reordered progress report as a Pandas DataFrame object
    """
    print('df_progress_rpt columns: ', df_progress_rpt.columns.to_list())
    # Start with the name column
    list_of_cols = [cols.name]

    for metric_code in metric_codes:
        # Reorder the metric colum and improvement metric together
        list_of_cols.append(metric_code)
        list_of_cols.append(metric_code + metric_code_append_txt)

    # Reorder the columns in the dataframe
    df_progress_rpt = df_progress_rpt[list_of_cols]

    return df_progress_rpt


        

if __name__ == '__main__':

    # Generate the elementary DEOs progress report
    generate_ceo_rev_deo_progress_report(school_levels.ELEMENTARY)

    # Generate the secondary DEOs progress report
    generate_ceo_rev_deo_progress_report(school_levels.SECONDARY)

