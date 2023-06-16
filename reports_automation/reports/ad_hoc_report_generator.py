"""
Module with generator functions to generate ad hoc reports
"""

import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import utilities.file_utilities as file_utilities
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

    # Rename the column names to standard format
    for df_data in df_data_set.values()
        column_cleaner.standardise_column_names(df_data)


    # Check if there is a custom logic to be executed before generating this report
    if (report_config['custom_base_report']):
        # Get the name of the module
        report_module_name = importlib.import_module('ad_hoc.' + report_config['report_name'])

    # Call the function with the custom logic for the report
    cust_logic_func = getattr(report_module_name, 'custom_logic')
    df_base_report = cust_logic_func(df_data_set)

    print('df_data_set: ', df_data_set)



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

    ranking_args = report_config['summary_args']
    if ranking_args is not None:
        # Get relative performance data by diving a config indicated numerator column against denominator column
        df_data_grouped[metric_col_name] = df_data_grouped[num_col] / df_data_grouped[den_col]

    if summary_args['sort']:
        df_data_grouped.sort_values(by=[metric_col_name], inplace=True, ascending=summary_args['ascending'])

    return df_data_grouped


def save_report(report_config: dict, df_report):
    """
    Function to save the generated ad hoc report in the current day - month folder

    Parameters:
    ----------
    report_config: dict
        Dictionary with the report configuration information
    df_report: DataFrame
        Pandas DataFrame object of the final data to be saved as a report.
    """
    dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
    file_utilities.save_to_excel({'Report': adhoc_report}, 'teacher_leave_absence_update.xlsx', dir_path)

    