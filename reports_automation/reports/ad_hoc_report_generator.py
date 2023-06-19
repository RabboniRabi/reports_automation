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

    # Update the config dictionary to resolve the variable names
    report_config = _update_config_dict(report_config)

    # Rename the column names to standard format
    for df_data in df_data_set.values()
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
        first_dataset = source_configs[0]
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


def _update_config_dict(report_config: dict):
    """
    Helper function to update the report configuration read from the JSON configuration.
    As variable names are stored as strings in JSON, the values mapped to these
    names dont resolve automatically and need to be updated.

    Parameters:
    ----------
    report_config: dict
        The ranking arguments fetched from the JSON configuration
    Returns:
    --------
    Updated report configuration dictionary
    """

    # Update the variable name strings in the merge sources configs
    for merge_source_config_name in report_config['merge_sources_configs'].keys():
        # Update the list of columns to join on
        updated_list = cols.get_values(merge_source_config_name['join_on'])
        merge_source_config_name['join_on'] = updated_list

    # Update the variable name strings in the summary sheets arguments
    for summary_sheet_arg in report_config['summary_sheets_args']:
        # Update the list of columns to group the data on
        updated_list = cols.get_values(summary_sheet_arg['grouping_levels'])
        summary_sheet_arg['grouping_levels'] = updated_list

    return report_config
        




    