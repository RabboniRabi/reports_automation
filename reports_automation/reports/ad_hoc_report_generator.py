"""
Module with generator functions to generate ad hoc reports
"""

import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.report_utilities as report_utilities
import utilities.report_format_utilities as report_format_utilities
import importlib
import data_cleaning.column_cleaner as column_cleaner
import readers.data_fetcher as data_fetcher
import readers.config_reader as config_reader

def get_report(report_config: dict, save_source:bool=False):
    """
    Function to generate the ad hoc report for a metric with given report configuration. 

    The final report can have multiple sheets each with a different summary of the data
    generated using the configuration provided. 

    The base report can also be included as another sheet for reference.

    Parameters:
    ----------
    report_config: dict
        Dictionary with the report configuration information
    save_source: bool  
        Flag indicating if copy of source data fetched from DB needs to be saved. Default is false.

    Returns:
    --------
    The generated ad hoc report summaries as a dictionary of Pandas DataFrame objects
    """

    if report_config is None:
        # No report configuration was found.
        sys.exit('No report configuration found. Cannot generate the report!')

    # Update the config dictionary to resolve the variable names
    report_config = cols.update_nested_dictionaries(report_config)

    # Get the base data
    df_base_report = _get_data_for_ad_hoc_report(report_config, save_source)

    #file_utilities.save_to_excel({'base_report': df_base_report}, 'df_base_report.xlsx')

    # Create report summary sheets from base data for given summary sheets configurations
    summary_sheets_args = report_config['summary_sheets_args']
    df_reports = _get_summary_sheets(df_base_report, summary_sheets_args)   
    
    # Add the base report to the final report if needed
    if report_config['include_base_report']:
        df_reports['base_report'] = df_base_report


    return df_reports
    

def _get_data_for_ad_hoc_report(report_config: dict, save_source:bool=False):
    """
    Helper function to fetch the base data for the ad hoc report.
    Depending on the configuration, data can be custom fetched,
    fetched from a single configured source or multiple sources, 
    each of which can either be from an Excel file or a DB query.

    In case of multiple sources, if data combination type (merge, concat, etc.)
    is provided in the config, data is combined. Data can also
    be custom combined if the 'custom_data_combine' flag is true in the config.
    In this case, the module in ad hoc corresponding to the name in the report config
    is called.

    Parameters:
    -----------
    report_config: dict
        Dictionary with the report configuration information
    save_source: bool  
        Flag indicating if copy of source data fetched from DB needs to be saved. Default is false.
    
    Returns:
    --------
    Pandas DataFrame object of base report data
    """

    # Get the source config
    source_config = report_config['source_config']

    # Check if custom data fetch is true
    if report_config['custom_data_fetch']:
        """
        Call the custom_data_fetch function in the module corresponding to the config
        and get the fetched data.
        """
        # Get the name of the module
        report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])

        # Call the function with the custom logic for the report
        cust_logic_func = getattr(report_module_name, 'custom_data_fetch')
        df_base_report = cust_logic_func()
    else:
        # Check and get data from single source configuration or multiple configurations
        if 'sources' in source_config:
            # Get the multiple source data as a dictionary of dataframe objects
            df_data_set = data_fetcher.get_data_set_from_config(source_config, save_source)
            
            # Rename the column names to standard format
            for df_data in df_data_set.values():
                column_cleaner.standardise_column_names(df_data)

            # Check if custom combine data flag is true
            if(source_config['custom_data_combine']):
                """
                Call the custom_data_combine function in the module corresponding to the config
                which will do the custom processing of the data set and return a Pandas DataFrame object.
                """
                # Get the name of the module
                report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])

                # Call the function with the custom logic for the report
                cust_logic_func = getattr(report_module_name, 'custom_data_combine')
                df_base_report = cust_logic_func(df_data_set)

            # else if config is provided, combine the data set into a single dataframe object
            elif ('combine_data_configs' in source_config):
                df_base_report = report_utilities.combine_multiple_datasets(df_data_set, source_config['combine_data_type'], \
                                source_config['combine_data_configs'])
            else:
                # No configuration for merge multiple sources was found.
                sys.exit('Multiple data sources given, but no corresponding combine_data_configs found!')
        elif 'source_file_name' or 'query_file_name' in source_config:
            # Get the single source data as a dataframe object
            df_data = data_fetcher.get_data_from_config(source_config, save_source)
            
            # Rename the column names to standard format
            df_base_report = column_cleaner.standardise_column_names(df_data)
        else: 
            # No source configuration was found.
            sys.exit('No source configuration(s) found!')

    return df_base_report


def _get_summary_sheets(df_base_report, summary_sheets_args):
    """
    Internal helper function to get summaries of data at different levels.

    Data will typically be grouped using the configuration for each summary 
    sheet to be created. Data in the summary can be sorted by a given value.
    Data can also be ranked.

    Parameters:
    -----------
    df_base_report: Pandas DataFrame
        The base data from which summaries are to be extracted
    summary_sheets_args: dict
        Dictionary of arguments required to create summaries of data

    Returns:
    -------
    Dictionary of Pandas DataFrame objects containing data summaries
    """

    # Declare a dictionary to hold all the summary sheet data
    df_reports = {}

    #print('df_base_report columns: ', df_base_report.columns.to_list())

    
    
    # For summary sheet configuration
    for summary_sheet_args in summary_sheets_args:

        if summary_sheet_args["custom_summary"]:
            # Call the custom method in the custom module for the script to create the summary report
            # Get the name of the module
            report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])
            # Call the function with the custom logic for the report
            cust_summary_func = getattr(report_module_name, summary_sheet_args["summary_sheet_code"])
            df_summary = cust_summary_func(df_base_report, summary_sheet_args)
        else:
            # Group the base report to the given grouping levels and aggregate given columns
            try:
                df_summary = df_base_report.groupby(summary_sheet_args['grouping_levels']).agg(summary_sheet_args['agg_dict'])
            except KeyError as err:
                print('One of the grouping keys (column) not found. column keys in data are: ', df_base_report.columns.to_list())
                sys.exit(err)

        # Sort and rank data if configuration is given
        ranking_config = summary_sheet_args['ranking_config']
        if ranking_config is not None and bool(ranking_config):
            df_summary = ranking_utilities.calc_ranking(df_summary, ranking_config)

        # Add the summary to the dictionary of data reports
        df_reports[summary_sheet_args['summary_sheet_code']] = df_summary

    return df_reports



        

def save_report(report_name: str, df_reports_dict):
    """
    Function to save the generated ad hoc report in the current day - month folder

    Parameters:
    ----------
    report_config: str
        The name to save as a report
    df_report: DataFrame dictionary
        Dictionary of report name key - Pandas DataFrame object value  pairs of the final data to be saved as a report.
    """
    dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
    file_utilities.save_to_excel(df_reports_dict, report_name+'.xlsx', dir_path)



def generate_format_save_report(report_code):
    """
    Function to generate, format and save the ad hoc report for a given report code/name. 

    Parameters:
    ----------
    report_code: str
        The name/code of the report/metric to fetch the Ad Hoc report for
    """

    # Get the overall configuration for the report code
    report_config = config_reader.get_adhoc_config(report_code)

    # Get the ad hoc report
    ad_hoc_rpt = get_report(report_config, save_report)

    # Format and save the report
    report_format_utilities.format_ad_hoc_report_and_save(
        ad_hoc_rpt, report_config['summary_sheets_args'], report_config['report_name']+'.xlsx')

