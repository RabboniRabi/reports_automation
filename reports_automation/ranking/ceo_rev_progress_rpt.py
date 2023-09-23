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
    based on improvement/decrease in ranks for each metric compared
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
                                
    curr_month_metric_codes  = df_curr_month_ranks[cols.metric_code].unique()

    # Filter out the metrics with zero weightage for the month
    metric_weightage_dict = weightage_fetcher.fetch_ceo_rev_metric_ranking_weightages(deo_lvl)
    metrics_to_omit = []
    for metric_code in curr_month_metric_codes:
        if metric_weightage_dict[metric_code] == 0:
            metrics_to_omit.append(metric_code)

    df_curr_month_ranks = utilities.filter_dataframe_not_in_column(\
                                        df_curr_month_ranks, cols.metric_code, metrics_to_omit)

    # Get the data in progress report format
    df_curr_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_curr_month_ranks)

    # Testing
    #file_utilities.save_to_excel({'test': df_curr_month_rpt}, 'df_curr_month_rpt.xlsx')
    

    # Get the previous month data
    prev_month = utilities.get_prev_month()
    prev_month_year = utilities.get_year_of_prev_month()
    df_prev_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [prev_month], [int(prev_month_year)])

    # Filter out the metrics with zero weightage for the current month from the previous month
    df_prev_month_ranks = utilities.filter_dataframe_not_in_column(\
                                        df_prev_month_ranks, cols.metric_code, metrics_to_omit)

    
    # Get the data in progress report format
    df_prev_month_rpt = ranking_utilities.build_metric_wise_ranking_report(df_prev_month_ranks)

    # Testing
    #file_utilities.save_to_excel({'test': df_prev_month_rpt}, 'df_prev_month_rpt.xlsx')

    metric_code_append_txt = '_improvement'


    # Get the improvement in ranks for each metric from previous month
    df_improv = _get_metric_code_wise_improvement(df_curr_month_rpt, \
                            df_prev_month_rpt, curr_month_metric_codes, metric_code_append_txt)

    # Testing
    #file_utilities.save_to_excel({'test': df_improv}, 'df_improv.xlsx')

    # Merge the rank improvement values data with the current month ranks
    df_curr_month_progress_rpt = df_curr_month_rpt.merge(df_improv, how='left', on=[cols.name])

    # Get the metrics with non zero weightage
    non_zero_weight_metrics = np.subtract(np.array(curr_month_metric_codes), np.array(metrics_to_omit)).tolist()

    # Reorder the metric codes and their corresponding improvement columns together
    df_curr_month_progress_rpt = _reorder_progress_report_cols(df_curr_month_progress_rpt, \
                                    non_zero_weight_metrics, metric_code_append_txt)
    
    """Format the report to visually highlight improvements"""

    dir_path = file_utilities.get_progress_reports_dir()

    # Get the xlsxwriter object of the data to be formatted and saved
    writer = file_utilities.get_xlsxwriter_obj({deo_lvl.value:df_curr_month_progress_rpt}, \
                       'DEO_' +  deo_lvl.value + '_' + curr_month +  '_progress_rpt.xlsx', dir_path)

    workbook = writer.book
    worksheet = workbook.get_worksheet_by_name(deo_lvl.value)

    # Get the column names of the metrics' improvement
    metric_codes_improv_names = [f'{x}'+ metric_code_append_txt for x in curr_month_metric_codes]


    # Get the format configs
    progress_rpt_format_configs = config_reader.get_misc_rpt_config('CEO_REV_PRG_RPT_FRMT')
    format_dicts_list = progress_rpt_format_configs['format_dicts_list']

    # Update the columns in the format_dicts_list
    for format_dict in format_dicts_list:
        format_dict['columns'] = metric_codes_improv_names

    # Apply the formatting
    format_utilities.apply_formatting(format_dicts_list, df_curr_month_progress_rpt, worksheet, workbook, start_row=1)
    
    writer.save()


    # testing
    #file_utilities.save_to_excel({'test': df_curr_month_progress_rpt}, 'df_curr_month_progress_rpt.xlsx')



def _get_metric_code_wise_improvement(df_curr, df_prev, metric_codes:list, metric_code_append_txt:str):
    """
    Internal helper function to get the improvement in rank/values for 
    each metric code column in current dataframe from previous dataframe:

    Parameters:
    -----------
    df_curr: Pandas DataFrame
        The current data
    df_prev: Pandas DataFrame
        The previous data
    metric_codes: list
        The list of metric codes
    metric_code_append_txt: str
        Optional text to append to each of the metric code column names.
        Eg: '_improvment'

    Returns:
    --------
    DataFrame with improvement values for each metric code
    """

    # Sort the data
    df_curr = df_curr.sort_values(by=cols.name).reset_index()
    df_prev = df_prev.sort_values(by=cols.name).reset_index()

    #print('df_curr post sorting: ', df_curr)
    #print('df_prev post sorting: ', df_prev)

    df_improv = df_curr.copy()
    #print('df_improv before updating: ', df_improv)
    rename_dict = {}

    for metric_code in metric_codes:
        if metric_code in df_prev:
            #print('for ', metric_code, 'df_curr is: ', df_curr[metric_code])
            #print('for ', metric_code, 'df_prev is: ', df_prev[metric_code])
            df_improv[metric_code] =  df_prev[metric_code] - df_curr[metric_code]
            #print('df_improv[metric_code] is: ', df_improv[metric_code])
        else:
            df_improv[metric_code] = 0

        # If text to append is given, add the metric to the rename dict
        if metric_code_append_txt is not None:
            rename_dict[metric_code] = metric_code + '_improvement'

    # Rename the metric code column names to the text appended column names
    df_improv.rename(columns=rename_dict, inplace=True)

    #print('df_improv: ', df_improv)

    return df_improv

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

