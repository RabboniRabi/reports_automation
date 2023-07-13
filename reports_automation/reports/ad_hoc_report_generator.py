"""
Module with generator functions to generate ad hoc reports
"""

import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.update_variable_names_utilities as update_variable_names_utilities
import importlib
import data_cleaning.column_cleaner as column_cleaner
import data_fetcher



def get_report(report_config: dict, df_data_set):
    """
    Function to generate the ad hoc report for a metric with given report configuration. 

    Parameters:
    ----------
    report_config: dict
        Dictionary with the report configuration information
    save_source: bool  
        Flag indicating if source data fetched needs to be saved. Default is false.

    Returns:
    --------
    The generated ad hoc report as a Pandas DataFrame object.
    """

    if report_config is None:
        # No report configuration was found.
        sys.exit('No report configuration found. Cannot generate the report!')

    # Update the config dictionary to resolve the variable names
    report_config = update_variable_names_utilities.update_ad_hoc_config_dict(report_config)

    # Rename the column names to standard format
    for df_data in df_data_set.values():
        column_cleaner.standardise_column_names(df_data)

    # Get the merge sources configs
    merge_sources_configs = report_config['merge_sources_configs']

    # Check if there is a custom logic to be executed before generating this report
    if (report_config['custom_base_report']):
        # Get the name of the module
        report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])

        # Call the function with the custom logic for the report
        cust_logic_func = getattr(report_module_name, 'custom_base_report')
        df_base_report = cust_logic_func(df_data_set, merge_sources_configs)
    else:
        # Merge with the first dataset the remaining source datasets to form the base report
        source_configs = report_config['source_configs']
        merge_sources_configs = report_config['merge_sources_configs']
        df_base_report = pd.DataFrame()
        for source_config_index in range(0, len(source_configs)):
            # If data is first dataset, it becomes the base report
            if source_config_index == 0:
                df_base_report = source_configs[source_config_index]
            else:
                # Merge the remaining source datasets together, with the data being left joined with the base report
                # Get the name of the source.
                # This name will be used to fetch the corresponding configuration in merge_sources_configs
                source_name = source_configs[source_config_index]['source_name']
                merge_source_config = merge_sources_configs[source_name]
                df_base_report = df_base_report.merge(source_configs[source_config_index], \
                                    how=merge_source_config['join_on'], on=merge_source_config['merge_type'])


    print('df_base_report: ', df_base_report)

    file_utilities.save_to_excel({'base_report': df_base_report}, 'df_base_report.xlsx')

    # Create report summary sheets from base data for given summary sheets configurations
    summary_sheets_args = report_config['summary_sheets_args']
    df_reports = {}
    
    # For summary sheet configuration
    for summary_sheet_args in summary_sheets_args:
        if summary_sheet_args["custom_summary"]:
            # Call the custom method in the custom module for the script to create the summary report
            # Get the name of the module
            report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])
            # Call the function with the custom logic for the report
            cust_summary_func = getattr(report_module_name, summary_sheet_args["summary_sheet_code"])
            df_base_report = cust_summary_func(df_base_report, summary_sheet_args)
        else:
            # Group the base report to the given grouping levels and aggregate given columns
            df_summary = df_base_report.groupby(summary_sheet_args["grouping_levels"]).agg(summary_sheet_args["agg_dict"])

        
        # Calculate ranking if configuration is given
        ranking_args = summary_sheet_args['ranking_args']
        if ranking_args is not None and bool(ranking_args):
            df_summary = ranking_utilities.calc_ranking(df_summary, None, ranking_args)

        df_reports[summary_sheet_args["summary_sheet_name"]] = df_summary
    
    # Add the base report to the final report if needed
    if report_config['include_base_report']:
        df_reports['base_report'] = df_base_report

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



    