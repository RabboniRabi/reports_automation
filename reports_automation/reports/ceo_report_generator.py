"""
Module with generator functions to generate CEO reports
"""

import sys
sys.path.append('../')

import utilities.report_utilities as report_utilities
import utilities.file_utilities as file_utilities
import utilities.report_format_utilities as report_format_utilities
import readers.data_fetcher as data_fetcher
import readers.config_reader as config_reader
import utilities.column_names_utilities as cols
import importlib

from ceo_report_levels import CEOReportLevels as ceo_report_levels
from enums.school_levels import SchoolLevels as school_levels
from enums.ranking_types import RankingTypes as ranking_types
import data_cleaning.column_cleaner as column_cleaner
import warnings
warnings.filterwarnings('ignore')


def get_ceo_report_raw_data(report_config: dict, save_source=False):
    """
    Function to generate the raw data for CEO reports. This data would be
    the raw data processed and merged with BRC-CRC mapping data.
    
    The processing can be pre-processing, post-processing or both. 
    This is determined in the configuration provided. 

    The function calls the processing functions in the corresponding module for the report
    as pre and post processing wil be unique to each report

    Parameters:
    ----------
    report_config: dict
        Dictionary with the report configuration information

    Returns:
    -------
        Raw data processed and merged with BRC-CRC mapping as a DataFrame object.
    """

    if report_config is None:
        # No report configuration was found.
        sys.exit('No report configuration found. Cannot generate the report!')

    # Update the variable names in the report config JSON
    report_config = cols.update_nested_dictionaries(report_config)

    # Get the source configuration
    source_config = report_config['source_config']

    # Check and get data from single source configuration or multiple configurations
    if 'sources' in source_config:
        # Get the multiple source data as a dictionary of dataframe objects
        df_data_set = data_fetcher.get_data_set_from_config(source_config, save_source)
        
        # Rename the column names to standard format
        for df_data in df_data_set.values():
            column_cleaner.standardise_column_names(df_data)

        # Combine the data set into a single dataframe object
        if ('combine_data_configs' in source_config):
            df_data = report_utilities.combine_multiple_datasets(df_data_set, source_config['combine_data_type'], \
                             source_config['combine_data_configs'])
        else:
            # No configuration for merge multiple sources was found.
            sys.exit('Multiple data sources given, but no corresponding combine_data_configs found!')
    elif 'source_file_name' or 'query_file_name' in source_config:
        # Get the single source data as a dataframe object
        df_data = data_fetcher.get_data_from_config(source_config, save_source)
        
        # Rename the column names to standard format
        df_data = column_cleaner.standardise_column_names(df_data)
    else: 
        # No source configuration was found.
        sys.exit('No source configuration(s) found!')


    # Check if pre-processing before merging with BRC-CRC mapping is required
    if (report_config['pre_process_brc_merge']):
        print('Going to pre-process data')
        # Call the custom pre-processing function for the report
        report_module_name = importlib.import_module('ceo_reports.' + report_config['report_name'])
        pre_proc_func = getattr(report_module_name, 'pre_process_BRC_merge')
        df_data = pre_proc_func(df_data)


    # Merge the data with BRC-CRC mapping
    brc_merge_config = report_config['brc_merge_config']
    if brc_merge_config is None:
        # No BRC merge configuration was found
        sys.exit('BRC Merge configuration not provided for report: ', report_config['report_name'])

    df_data = report_utilities.map_data_with_brc(df_data, brc_merge_config)

     # Check if post-processing after merging with BRC-CRC mapping is required
    if (report_config['post_process_brc_merge']):
        # Call the custom post-processing function for the report
        report_module_name = importlib.import_module('ceo_reports.' + report_config['report_name'])
        post_proc_func = getattr(report_module_name, 'post_process_BRC_merge')
        df_data = post_proc_func(df_data) 


    return df_data


def get_ceo_report(report_config: dict, school_level, report_level, save_source=False):
    """
    Function to generate the CEO report for a metric with given report configuration. 

    The report can be generated for Elementary or Secondary school level.

    The report is also generated for given reporting level

    Parameters:
    ----------
    report_config: dict
        Dictionary with the report configuration information
    school_level: str
        The school level to filter and generate the report for (Elementary/Secondary)
    report_level: str
        The level of report to be generated. (Unranked/Ranked)
    save_source: bool  
        Flag indicating if source data fetched needs to be saved. Default is false.

    Returns:
    --------
    The generated CEO report as a Pandas DataFrame object.
    """

    # Update the variable names in the report config JSON
    config = cols.update_nested_dictionaries(config)

    # Get the raw data merged with the BRC-CRC mapping
    df_data = get_ceo_report_raw_data(report_config, save_source)


    # Get the report metric code and category
    metric_code = report_config['report_code']
    metric_category = report_config['report_category']
    report_name = report_config['report_name']

    # Check if school level for report is Elementary
    if school_level == school_levels.ELEMENTARY.value:

        # Get the ranking arguments for Elementary report
        elem_report_config = report_config['elementary_report']

        # Check that the configuration for elementary report exists
        if elem_report_config is None:
            # No elementary report configuration was found
            sys.exit('Elementary report configuration not provided for report: ', report_config['report_name'])

        # Call the helper function to generate the elementary report
        report = _generate_elem_report(df_data, elem_report_config, report_name, report_level, metric_code,
                                       metric_category)

        return report
    
    # Check if school level for report is Secondary
    if school_level == school_levels.SECONDARY.value:

        # Get the ranking arguments for secondary report
        sec_report_config = report_config['secondary_report']

        # Check that the configuration for secondary report exists
        if sec_report_config is None:
            # No Secondary report configuration was found
            sys.exit('Secondary report configuration not provided for report: ', report_config['report_name'])

        # Call the helper function to generate the elementary report
        report = _generate_sec_report(df_data, sec_report_config, report_name, report_level, metric_code, metric_category)

        return report

def generate_all(generate_fresh: bool = True):
    """
    Function to generate all configured and active reports for CEO review in one shot.

    This function will iterate through each active configuration, call the get_ceo_report function
    to generate the report, format the report and save.

    Parameters:
    ----------
    generate_fresh: bool
        Flag to indicate if all reports for the month needed need to be generated fresh.
        Default is True. If False, already generated reports for the month are ignored.
    """
    active_configs = config_reader.get_all_active_ceo_review_configs()

    for config in active_configs:

        # Update the variable names in the report config JSON
        config = cols.update_nested_dictionaries(config)

        report_name = config['report_name']

        # Define elementary report name and get existence flag and get elementary report configs
        elem_report_name = config['report_desc'] + '-Elementary.xlsx'
        curr_month_elem_ceo_rpts_dir_path = file_utilities.get_curr_month_elem_ceo_rpts_dir_path()
        elem_file_exists = file_utilities.file_exists(elem_report_name, curr_month_elem_ceo_rpts_dir_path)

        # Get the arguments for Elementary report
        elem_report_config = config['elementary_report']
        # Check that the configuration for elementary report exists
        if elem_report_config is None:
            # No elementary report configuration was found
            sys.exit('Elementary report configuration not provided for report: ', report_name)
        generate_elem = elem_report_config['generate_report']
        
        # Define secondary report name and get existence flag and get secondary report configs
        sec_report_name = config['report_desc'] + '-Secondary.xlsx'
        curr_month_secnd_ceo_rpts_dir_path = file_utilities.get_curr_month_secnd_ceo_rpts_dir_path()
        sec_file_exists = file_utilities.file_exists(sec_report_name, curr_month_secnd_ceo_rpts_dir_path)
        # Get the ranking arguments for Secondary report
        sec_report_config = config['secondary_report']
        # Check that the configuration for secondary report exists
        if sec_report_config is None:
            # No Secondary report configuration was found
            sys.exit('Secondary report configuration not provided for report: ', report_name)
        generate_sec = sec_report_config['generate_report']

        # Check if elementary and secondary reports for current configuration needs to be generated
        if elem_file_exists and sec_file_exists and not generate_fresh:
            print('Report already generated for', config['report_name'])
            continue
        elif (elem_file_exists and not generate_fresh) and not generate_sec:
            print('Report already generated for', config['report_name'])
            continue
        elif (sec_file_exists and not generate_fresh) and not generate_elem:
            print('Report already generated for', config['report_name'])
            continue


        print('Generating report for: ', config['report_name'], '...')

        # Get the report metric code and category
        metric_code = config['report_code']
        metric_category = config['report_category']

        # Get the raw data merged with the BRC-CRC mapping
        df_data = get_ceo_report_raw_data(config, True)

        # Elementary Report
        # Check if elementary report needs to be generated
        if (generate_fresh or not elem_file_exists) :

            if elem_report_config['generate_report']:
                # Call the helper function to generate the elementary report
                elem_report = _generate_elem_report(df_data, elem_report_config, report_name\
                    , ceo_report_levels.RANKED, metric_code, metric_category)

                # Check if formatting needs to be done
                format_config = elem_report_config['format_config']
                if format_config is not None:
                    # Call review view utilities to format and save the report
                    report_format_utilities.format_ceo_review_report(elem_report\
                            , format_config, elem_report_config['ranking_config']\
                            , metric_code, elem_report_name, curr_month_elem_ceo_rpts_dir_path)
                else:
                    # Save the report without any formatting
                    file_utilities.save_to_excel({metric_code: elem_report}, elem_report_name\
                            , curr_month_elem_ceo_rpts_dir_path)
        
        # Secondary Report
        # Check if secondary report needs to be generated
        if (generate_fresh or not sec_file_exists):

            if sec_report_config['generate_report']:

                # Call the helper function to generate the elementary report
                sec_report = _generate_sec_report(df_data, sec_report_config, report_name, ceo_report_levels.RANKED, metric_code, metric_category)

                #sec_report = get_ceo_report(config, 'Secondary', ceo_report_levels.RANKED)

                # Check if formatting needs to be done
                format_config = sec_report_config['format_config']
                if format_config is not None:
                    # Call review view utilities to format and save the report
                    report_format_utilities.format_ceo_review_report(sec_report\
                            , format_config, sec_report_config['ranking_config'], metric_code, sec_report_name, curr_month_secnd_ceo_rpts_dir_path)
                else:
                    # Save the report without any formatting
                    file_utilities.save_to_excel({metric_code: sec_report}, sec_report_name, curr_month_secnd_ceo_rpts_dir_path)


def _generate_elem_report(ceo_rpt_raw_data, elem_report_config:dict, report_name:str, report_level:str, metric_code, metric_category):
    """
    Internal helper function to generate the elementary report for given ceo report raw data

    Parameters:
    ------------
    ceo_rpt_raw_data: Pandas DataFrame
        The raw data in CEO report format (merged with BRC CRC Mapping)
    elem_report_config: dict
        The configuration to generate the elementary report
    report_name: dict
        The name of the report which will be used to call the custom unranked report function
        for the report if needed
    report_level: str
        The level of report to be generated. (Unranked/Ranked)
    metric_code: str
        The report/metric code
    metric_Category: str
        The report/metric category

    Returns:
    --------
    The generated secondary report as a Pandas DataFrame object.
    """

    # Filter the data to Elementary school type
    ceo_rpt_raw_data = ceo_rpt_raw_data[ceo_rpt_raw_data[cols.school_level].isin([cols.elem_schl_lvl])]

    # Get the arguments for generating elementary unranked report
    un_ranked_report_config  = elem_report_config['un_ranked_report_args']

    # Get the columns to group by
    grouping_cols = un_ranked_report_config['grouping_cols']

    # Get the aggregate functions to apply on the grouped columns
    agg_dict = un_ranked_report_config['grouping_agg_dict']

    # If a custom unranked report is configured to be called
    if (un_ranked_report_config['custom_unranked_report']):
        # Call the corresponding function for the report
        report_module_name = importlib.import_module('ceo_reports.' + report_name)
        cust_rpt_func = getattr(report_module_name, 'get_unranked_elem_report')
        report = cust_rpt_func(ceo_rpt_raw_data, grouping_cols, agg_dict)
    else:
        # Just group the data to grouping level
        report = ceo_rpt_raw_data.groupby(grouping_cols, as_index=False).agg(agg_dict)

    # Check if ranking is required in report
    if report_level == ceo_report_levels.RANKED.value or report_level == ceo_report_levels.RANKED:
        # Generate ranking and update report
        ranking_dict = elem_report_config['ranking_config']
        # Get the elementary ranked report
        report = report_utilities.get_elem_ranked_report(report, ranking_dict, metric_code, metric_category)

    return report


def _generate_sec_report(ceo_rpt_raw_data, sec_report_config:dict, report_name, report_level:str, metric_code, metric_category):
    """
    Internal helper function to generate the secondary report for given ceo report raw data

    Parameters:
    ------------
    ceo_rpt_raw_data: Pandas DataFrame
        The raw data in CEO report format (merged with BRC CRC Mapping)
    sec_report_config: dict
        The configuration to generate the secondary report
    report_name: dict
        The name of the report which will be used to call the custom unranked report function
        for the report if needed
    report_level: str
        The level of report to be generated. (Unranked/Ranked)
    metric_code: str
        The report/metric code
    metric_Category: str
        The report/metric category

    Returns:
    --------
    The generated secondary report as a Pandas DataFrame object.
    """
    # Filter the data to secondary school type
    ceo_rpt_raw_data = ceo_rpt_raw_data[ceo_rpt_raw_data[cols.school_level].isin([cols.scnd_schl_lvl])]

    # Get the arguments for generating secondary unranked report
    un_ranked_report_config  = sec_report_config['un_ranked_report_args']

    # Get the columns to group by
    grouping_cols = un_ranked_report_config['grouping_cols']

    # Get the aggregate functions to apply on the grouped columns
    agg_dict = un_ranked_report_config['grouping_agg_dict']

    # If a custom unranked report is configured to be called
    if (un_ranked_report_config['custom_unranked_report']):
        # Call the corresponding function for the report
        report_module_name = importlib.import_module('ceo_reports.' + report_name)
        cust_rpt_func = getattr(report_module_name, 'get_unranked_sec_report')
        report = cust_rpt_func(ceo_rpt_raw_data, grouping_cols, agg_dict)
    else:
        # Just group the data to grouping level
        report = ceo_rpt_raw_data.groupby(grouping_cols, as_index=False).agg(agg_dict)

    # Check if ranking is required in report
    if report_level == ceo_report_levels.RANKED.value or report_level == ceo_report_levels.RANKED:
        # Generate ranking and update report
        ranking_dict = sec_report_config['ranking_config']
        # Get the secondary ranked report
        report = report_utilities.get_sec_ranked_report(report, ranking_dict, metric_code, metric_category)

    return report


# For testing
if __name__ == "__main__":
    generate_all(generate_fresh=False)
