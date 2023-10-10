"""
Module to create analysis reports with subject wise median and standard deviation
of SSLC data for each of a given list of metrics to analyse.
"""

import sys

import pandas as pd

sys.path.append('../')

import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import tenth_board_data_prep


def get_metric_subj_wise_med_sd_rpt(metric: str, df_dict_curr_yr: dict, df_dict_prev_yr: dict,
                                    median_agg_dict: dict, std_dev_agg_dict: dict):
    """
    Function to generate reports at state, district & block level for a given metric with
    subject wise data aggregated for median and standard deviation for
    current year and previous year data.

    Parameters:
    ---------
    metric: str
        The data analysis metric for which to generate the report for
    df_dict_curr_yr: dict
        Current year data as a dictionary of management-type : data
        key value pairs
    df_dict_prev_yr: dict
        Previous year data as a dictionary of management-type : data
        key value pairs
    median_agg_dict: dict
        Dictionary to be used to calculate median values for different levels
        of grouped data (state, district, block)
    std_dev_agg_dict: dict
        Dictionary to be used to calculate standard deviation values for different levels
        of grouped data (state, district, block)

    Returns:
    --------
    Dictionary of reports at state, district and block level
    """

    curr_yr = utilities.get_curr_year()
    prev_yr = utilities.get_prev_year()

    # Get block level report
    block_grouping_lvl = [cols.district_name, cols.block_name, cols.management, metric]
    # Get the report for current year
    blk_curr_yr = _get_grouping_lvl_med_sd(block_grouping_lvl, df_dict_curr_yr, median_agg_dict, std_dev_agg_dict)
    # Add year column
    blk_curr_yr[cols.year_col] = curr_yr
    # Sort the block report
    blk_curr_yr.sort_values(by=block_grouping_lvl, inplace=True)
    # Get the report for previous year
    blk_prev_yr = _get_grouping_lvl_med_sd(block_grouping_lvl, df_dict_prev_yr, median_agg_dict, std_dev_agg_dict)
    # Add year column
    blk_prev_yr[cols.year_col] = prev_yr
    # Sort the block report
    blk_prev_yr.sort_values(by=block_grouping_lvl, inplace=True)
    # concatenate current year and previous year report
    blk_rpt = pd.concat([blk_curr_yr, blk_prev_yr])



    # Get district level report
    district_grouping_lvl = [cols.district_name, cols.management, metric]
    # Get the report for current year
    district_curr_yr = _get_grouping_lvl_med_sd(district_grouping_lvl, df_dict_curr_yr, median_agg_dict,
                                                std_dev_agg_dict)
    # Add year column
    district_curr_yr[cols.year_col] = curr_yr
    # Sort the district report
    district_curr_yr.sort_values(by=district_grouping_lvl, inplace=True)

    # Get the report for previous year
    district_prev_yr = _get_grouping_lvl_med_sd(district_grouping_lvl, df_dict_prev_yr, median_agg_dict,
                                                std_dev_agg_dict)
    # Add year column
    district_prev_yr[cols.year_col] = prev_yr
    # Sort the district report
    district_prev_yr.sort_values(by=district_grouping_lvl, inplace=True)

    # concatenate current year and previous year report
    dist_rpt = pd.concat([district_curr_yr, district_prev_yr])


    # Get state level report
    state_grouping_lvl = [cols.management, metric]
    # Get the report for current year
    state_curr_yr = _get_grouping_lvl_med_sd(state_grouping_lvl, df_dict_curr_yr, median_agg_dict, std_dev_agg_dict)
    # Add year column
    state_curr_yr[cols.year_col] = curr_yr
    # Sort the state report
    state_curr_yr.sort_values(by=state_grouping_lvl, inplace=True)
    # Get the report for previous year
    state_prev_yr = _get_grouping_lvl_med_sd(state_grouping_lvl, df_dict_prev_yr, median_agg_dict, std_dev_agg_dict)
    # Add year column
    state_prev_yr[cols.year_col] = prev_yr
    # Sort the state report
    state_prev_yr.sort_values(by=state_grouping_lvl, inplace=True)
    # concatenate current year and previous year report
    state_rpt = pd.concat([state_curr_yr, state_prev_yr])


    df_metric_subj_wise_rpt = {'Block': blk_rpt, 'District': dist_rpt, 'State': state_rpt}

    # return report for metric
    return df_metric_subj_wise_rpt


def _get_grouping_lvl_med_sd(grouping_levels: list, df_dict: dict, median_agg_dict: dict, std_dev_agg_dict: dict):
    """
    Internal helper function to create a report of data grouped to given grouping level
    and median and standard deviation of specified columns calculated.

    Parameters:
    ----------
    grouping_levels: list
        Levels to group the data by
    df_dict: dict
        Data as a dictionary of management-type : data
        key value pairs
    median_agg_dict: dict
        Dictionary to be used to calculate median values for different levels
        of grouped data (state, district, block)
    std_dev_agg_dict: dict
        Dictionary to be used to calculate standard deviation values for different levels
        of grouped data (state, district, block)

    Returns:
    --------
    Report for metric at given grouping level
    """


    # Convert the mark columns to integers
    col_int_dict = {}
    for key in median_agg_dict.keys():
        col_int_dict[key] = 'int'
    for key in std_dev_agg_dict.keys():
        col_int_dict[key] = 'int'
    for key in df_dict.keys():
        df_dict[key] = df_dict[key].astype(col_int_dict)

    # Group the data and get the median values
    df_med = tenth_board_data_prep.get_grouping_level_data(df_dict.copy(), grouping_levels, median_agg_dict)

    # Rename student count and pass count to readable format
    df_med.rename(columns={cols.tot_stu:cols.brd_tot_stu_appr, cols.stu_pass:cols.brd_tot_stu_pass}, inplace=True)
    print('df_med columns: ', df_med.columns.to_list())
    # Group the data and get the standard deviation values
    df_sd = tenth_board_data_prep.get_grouping_level_data(df_dict.copy(), grouping_levels, std_dev_agg_dict)
    print('df_sd columns: ', df_sd.columns.to_list())

    # Merge median and standard deviation value for the grouped data
    df_med_sd = pd.merge(df_med, df_sd, how='inner', on=grouping_levels)

    # return the data
    return df_med_sd


def main():
    """
    Starting point of the script that calls the subject and metric wise report generation
    functions for each metric and saves the report.
    """

    # Fetch the configuration for creating the reports
    config = config_reader.get_config('10TH_SUBJ_ALL_METRICS_CONFIG', 'miscellaneous_configs')
    config = cols.update_nested_dictionaries(config)

    # Get the current year and previous year data set for all management types
    source_config_curr_yr = config['source_config_curr_yr']
    sources_curr_yr = data_fetcher.get_data_set_from_config(source_config_curr_yr, "miscellaneous_configs")

    sources_prev_yr = config['sources_prev_yr']
    sources_prev_yr = data_fetcher.get_data_set_from_config(sources_prev_yr, "miscellaneous_configs")

    # Data cleaning - excluding invalid values from the dataframe
    filter_dict = config['filter_dict']

    for key in sources_curr_yr.keys():
        sources_curr_yr[key] = utilities.filter_dataframe(sources_curr_yr[key], filter_dict, include=False)
    for key in sources_prev_yr.keys():
        sources_prev_yr[key] = utilities.filter_dataframe(sources_prev_yr[key], filter_dict, include=False)

    # Get the metrics to generate the reports for
    metrics = config['metrics']

    # Get the median aggregate dictionary to calculate median values in report
    median_agg_dict = config['agg_dict_median']

    # Get the standard deviation aggregate dictionary to calculate standard deviation values in report
    std_dev_agg_dict = config['agg_dict_std']

    # For each metric
    for metric in metrics:
        metric_report = get_metric_subj_wise_med_sd_rpt(metric, sources_curr_yr, sources_prev_yr,
                                                        median_agg_dict, std_dev_agg_dict)

        # Save the metric report
        dir_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('analysis')
        file_utilities.save_to_excel(metric_report, 'SSLC_' + metric + '_subj_wise_rpt.xlsx', dir_path=dir_path)


if __name__ == '__main__':
    main()
