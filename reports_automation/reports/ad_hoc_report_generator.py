"""
Module with generator functions to generate ad hoc reports
"""

import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import importlib

import data_fetcher



def get_report(report_config: dict, save_source:bool=False):
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

    source_config = report_config['source_config']
    df_data = data_fetcher.get_data_from_config(source_config, save_source)


    # Check if there is a custom logic to be executed before generating this report
    if (report_config['custom_logic']):
        # Get the name of the module
        report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])

        # Call the function with the custom logic for the report
        cust_logic_func = getattr(report_module_name, 'custom_logic')
        df_data = pre_proc_func(cust_logic_func)

    # Get the report summary arguments and update them as JSON to dict mapping is not clean with variables
    summary_args = report_config['summary_args']
    grouping_levels = cols.get_values(summary_args['grouping_levels'])
    agg_dict = cols.update_dictionary_var_strs(summary_args['agg_dict'])
    metric_col_name = cols.get_value(summary_args['metric_col_name'])
    num_col = cols.get_value(summary_args['num_col'])
    den_col = cols.get_value(summary_args['den_col'])

    # Update the boolean values for sorting and ascending flags
    summary_args['sort'] = summary_args['sort'] == 'True'
    summary_args['ascending'] = summary_args['ascending'] == 'True'

    # Group the data to grouping_level
    df_data_grouped = df_data.groupby(grouping_levels, as_index=False).agg(agg_dict)

    # Get relative performance data by diving a config indicated numerator column against denominator column
    df_data_grouped[metric_col_name] = df_data_grouped[num_col] / df_data_grouped[den_col]

    if summary_args['sort']:
        df_data_grouped.sort_values(by=[metric_col_name], inplace=True, ascending=summary_args['ascending'])

    return df_data_grouped

    