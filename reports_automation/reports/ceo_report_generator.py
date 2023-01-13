

import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.report_utilities as report_utilities
import data_fetcher
import utilities.column_names_utilities as cols
import importlib

from school_levels import SchoolLevels as school_levels
from ceo_report_levels import CEOReportLevels as ceo_report_levels
from ceo_report_ranking_types import CEOReportRankingTypes as ranking_types

import json
"""
========================================================================================================================
Module with functions will be the master code that will run the CEO reports in blocks/functions of code.
This will entail 2 main functions:
    1. Run all the code and generator all the reports in one go: generate_all():

    generate_all():
        active_configs = config_reader.get_Active_configs()
        for each active config
            ceo_raw_data = get_ceo_report_raw_data(config[code], 'raw data with brc-crc mapping', save_source=True)
            elementary_report = get_ceo_report(config[code], 'Elementary', 'ranked')
            secondary_report = get_ceo_report(config[code], 'Secondary', 'ranked')
            review_view_utilities.prepare_report_for_review(elementary_report)
            review_view_utilities.prepare_report_for_review(secondary_report)

    def get_ceo_report_raw_data(code, temp, param, save_source = False):
        config = config_reader.get_config(code)
        source_config = config['source_config']
        raw_data = data_fetcher.get_data_from_config(source_config)

a source config - > there are 2 options in the json -> if query name except OSerror -> excel file name -> except error in input

"""

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

    source_config = report_config['source_config']
    df_data = data_fetcher.get_data_from_config(source_config, save_source)

    print('columns in data read: ', df_data.columns.to_list())

    report_module_name = importlib.import_module('ceo_reports.' + report_config['report_name'])

    # Check if pre-processing before merging with BRC-CRC mapping is required
    if (report_config['pre_process_brc_merge']):
        print('Going to pre-process data')
        # Call the custom pre-processing function for the report
        pre_proc_func = getattr(report_module_name, 'pre_process_BRC_merge')
        df_data = pre_proc_func(df_data)

    # Merge the data with BRC-CRC mapping
    brc_merge_config = report_config['brc_merge_config']
    if brc_merge_config is None:
        # No BRC merge configuration was found
        sys.exit('BRC Merge configuration not provided for report: ', report_config['report_name'])

    # Update the config by replacing variable string names with corresponding values
    # This is done as the variable name in defined as a string in the JSON config
    join_on_vars = brc_merge_config['join_on']
    brc_merge_config['join_on'] = cols.get_values(join_on_vars)

    print('df_data columns: ', df_data.columns.to_list())
    print('brc_merge_config: ' , brc_merge_config['join_on'])
    
    df_data = report_utilities.map_data_with_brc(df_data, brc_merge_config)

     # Check if post-processing after merging with BRC-CRC mapping is required
    if (report_config['post_process_brc_merge']):
        # Call the custom post-processing function for the report
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

    # Get the raw data merged with the BRC-CRC mapping
    df_data = get_ceo_report_raw_data(report_config, save_source)

    print('raw data post merge columns: ', df_data.columns.to_list())
    print('raw data post merge: ', df_data)

    # Get the report metric code and category
    metric_code = report_config['report_code']
    metric_category = report_config['report_category']

    # Check if school level for report is Elementary
    if school_level == school_levels.ELEMENTARY.value:

        # Get the ranking arguments for Elementary report
        elem_report_config = report_config['elementary_report']

        # Check that the configuration for elementary report exists
        if elem_report_config is None:
            # No elementary report configuration was found
            sys.exit('Elementary report configuration not provided for report: ', report_config['report_name'])

        # Call the helper function to generate the elementary report
        report = _generate_elem_report(df_data, elem_report_config, report_level, metric_code, metric_category)

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
        report = _generate_sec_report(df_data, sec_report_config, report_level, metric_code, metric_category)

        return report

def _generate_elem_report(ceo_rpt_raw_data, elem_report_config:dict, report_level:str, metric_code, metric_category):
    """
    Internal helper function to generate the elementary report for given ceo report raw data

    Parameters:
    ------------
    ceo_rpt_raw_data: Pandas DataFrame
        The raw data in CEO report format (merged with BRC CRC Mapping)
    elem_report_config: dict
        The configuration to generate the elementary report
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
    # Update the values of column names to group by (To resolve string variable names).
    grouping_cols = cols.get_values(grouping_cols)

    # Get the aggregate functions to apply on the grouped columns
    agg_dict = un_ranked_report_config['grouping_agg_dict']
    # Update the keys in the aggregate dictionary as the string variable
    # names will not be resolved after being read from JSON
    agg_dict = cols.update_dictionary_var_strs(agg_dict)

    # If a custom unranked report is configured to be called
    if (un_ranked_report_config['custom_unranked_report']):
        # Call the corresponding function for the report
        report_module_name = importlib.import_module('ceo_reports.' + report_config['report_name'])
        cust_rpt_func = getattr(report_module_name, 'get_unranked_elem_report')
        report = cust_rpt_func(ceo_rpt_raw_data, grouping_cols, agg_dict)
    else:
        # Just group the data to grouping level
        report = ceo_rpt_raw_data.groupby(grouping_cols, as_index=False).agg(agg_dict)

    # Check if ranking is required in report
    if report_level == ceo_report_levels.RANKED.value:
        # Generate ranking and update report
        ranking_dict = elem_report_config['ranking_args']
        # Update the values in ranking argument
        ranking_dict = _update_ranking_args_dict(ranking_dict)
        # Get the elementary ranked report
        report = report_utilities.get_elem_ranked_report(report, ranking_dict, metric_code, metric_category)

    return report


def _generate_sec_report(ceo_rpt_raw_data, sec_report_config:dict, report_level:str, metric_code, metric_category):
    """
    Internal helper function to generate the secondary report for given ceo report raw data

    Parameters:
    ------------
    ceo_rpt_raw_data: Pandas DataFrame
        The raw data in CEO report format (merged with BRC CRC Mapping)
    sec_report_config: dict
        The configuration to generate the secondary report
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
    # Update the values of column names to group by (To resolve string variable names).
    grouping_cols = cols.get_values(grouping_cols)

    # Get the aggregate functions to apply on the grouped columns
    agg_dict = un_ranked_report_config['grouping_agg_dict']
    # Update the keys in the aggregate dictionary as the string variable
    # names will not be resolved after being read from JSON
    agg_dict = cols.update_dictionary_var_strs(agg_dict)

    # If a custom unranked report is configured to be called
    if (un_ranked_report_config['custom_unranked_report']):
        # Call the corresponding function for the report
        report_module_name = importlib.import_module('ceo_reports.' + report_config['report_name'])
        cust_rpt_func = getattr(report_module_name, 'get_unranked_sec_report')
        report = cust_rpt_func(ceo_rpt_raw_data, grouping_cols, agg_dict)
    else:
        # Just group the data to grouping level
        report = ceo_rpt_raw_data.groupby(grouping_cols, as_index=False).agg(agg_dict)

    # Check if ranking is required in report
    if report_level == ceo_report_levels.RANKED.value:
        # Generate ranking and update report
        ranking_dict = sec_report_config['ranking_args']
        # Update the values in ranking argument
        ranking_dict = _update_ranking_args_dict(ranking_dict)
        # Get the secondary ranked report
        report = report_utilities.get_sec_ranked_report(report, ranking_dict, metric_code, metric_category)

    return report



def _update_ranking_args_dict(ranking_args:dict):
    """
    Helper function to update the ranking arguments read from the JSON configuration.
    As variable names are stored as strings in JSON, the values mapped to these
    names dont resolve automatically and need to be updated.

    Parameters:
    ----------
    ranking_args: dict
        The ranking arguments fetched from the JSON configuration
    Returns:
    --------
    Updated ranking arguments dictionary
    """
    # Update the keys in the raking aggregation dict to resolve string variable names
    updated_ranking_args_dict = cols.update_dictionary_var_strs(ranking_args['agg_dict'])
    ranking_args['agg_dict'] = updated_ranking_args_dict

    # Update ranking value description
    ranking_val_desc = cols.get_value(ranking_args['ranking_val_desc'])
    ranking_args['ranking_val_desc'] = ranking_val_desc

    ranking_type = ranking_args['ranking_type']

    if ranking_type == ranking_types.PERCENT_RANKING.value:
        # Update the numerator and denominator columns
        num_col_val = cols.get_value(ranking_args['num_col'])
        ranking_args['num_col'] = num_col_val
        den_col_val = cols.get_value(ranking_args['den_col'])
        ranking_args['den_col'] = den_col_val

    return ranking_args
    
"""

    2. Generate Generate specific reports by calling a specific definition:

    for public use:
    ===============

        A. get_ceo_report_raw_data(report_code,raw_data_level):
            [file path: reports > ceo_report_generator.py]
        ---------------------------------------------------------
            Available raw_data_level-
                1. raw data: get_data(code)
                [file path:reports > data_fetcher.py ]
                2. processed_with_brc - (pre-processing - optional) + Merge + (post-processing - optional)
                

        B. get_ceo_report(report_code,report_type,report_level):
            (file path: reports > ceo_report_generator.py)
        ----------------------------------------------------------
            Available report_type-
                    (i) elementary
                    (ii) secondary

            Available raw_data_level-
                4. unranked: unranked_elementary_report()/unranked_secondary_report()
                5. ranked: ranked_elementary_report()/ranked_secondary_report()

    for internal use:
    =================
                6. format_save_elementary_report()/format_save_secondary_report()
                7. consolidate_and_index_report()

------------------------------------------------------------------------------------------------------------------------
Requirements apart from the functions:
    1. Report wise dictionary:
        This dictionary would have the list of all the reports, and the various calculations required for processing.
        These will be stored as the components required for each block/function.
    2. JSON structure for reporting:
        The JSON would store all report specific information. These would include the
        a. Code of the report
        b. Ranking Arguments (Sorting, Numerator, Denominator, Name of the metric, Ranking Value etc.)
        c. Input to decide whether or not to running the particular report
    3. Report Index Master:
        This would be a document that is available in both the elementary and secondary folders in the report_generated
        folder. It would be the updated list of reports and their corresponding report codes. This document will merge
        the final elementary and secondary reports generated, and hyperlink the individual reports to the Index sheet.
------------------------------------------------------------------------------------------------------------------------
Ripple Effects:
    1. The ranking master would get updated each time a report is generated. This will happen only when the generate_all
    function is run. As this would affect the rankings for each month, and must reflect the rank that was provided in
    the actual report shared.
    
========================================================================================================================
The module will work as blocks as mentioned above. The following is the list of blocks/functions that will collectively
arrive at the CEO Review Reports in a single file:
"""


def get_data_from_config(source_config_dict, save_source=False):

    """
    ------------------------------------------------------------------------------------------------------------------------
    2. pre_processing_data_before_brc_merge():
        Function:
            Using the df returned by get_source_data(), this function would ensure that the raw data is crunched down to a
            school level (using UDISE Code as the primary key). This would vary depending on level of the source data. 
            
            Parameters:

        Returns:
            The final df that will be used before mapping with the master BRC-CRC file. 

    ------------------------------------------------------------------------------------------------------------------------
    """

"""
------------------------------------------------------------------------------------------------------------------------
4. post_processing_data_after_brc_merge():
    Function:
        This function uses the mapped raw data and processes it further to bring to the required format before splitting
        it up into elementary or secondary reports.

        Parameters:

    Returns:
        The final processed data required before splitting the data up into elementary and secondary reports.
========================================================================================================================
5.a.(i). unranked_elementary_report():
   Function:
        This function uses the processed data and prepares the elementary report up to the ranking step.

        Parameters:

    Returns:
        The final elementary data that will be used for ranking the reports.
------------------------------------------------------------------------------------------------------------------------
5.a.(ii). ranked_elementary_report():
   Function:
       This function ranks the elementary report, whilst updating the ranking master as well.

        Parameters:

    Returns:
        The final elementary report that will be printed, and ready for formatting.
------------------------------------------------------------------------------------------------------------------------
5.b.(i). unranked_for_secondary_report():
   Function:
        This function uses the processed data and prepares the secondary report up to the ranking step.

        Parameters:

    Returns:
        The final secondary data that will be used for ranking the reports.
------------------------------------------------------------------------------------------------------------------------
5.b.(ii). ranked_secondary_report():
   Function:
       This function ranks the secondary report, whilst updating the ranking master as well.

        Parameters:

    Returns:
        The final secondary report that will be printed, and ready for formatting.
------------------------------------------------------------------------------------------------------------------------
6.a. format_save_elementary_report():
    Function:
        This function performs the following formatting actions specific to the elementary report:
        (i) Outlines
        (ii) Adding back ranks
        (iii) Font formatting
        (iv) Merging the top row for the heading
        (v) Adding a row for the column index

        Parameters:

    Returns:
        This is the report that will be saved into the elementary reports folder.
------------------------------------------------------------------------------------------------------------------------
6.b. format_save_secondary_report():
    Function:
        This function performs the following formatting actions specific to the secondary report:
        (i) Outlines
        (ii) Adding back ranks
        (iii) Font formatting
        (iv) Merging the top row for the heading
        (v) Adding a row for the column index

        Parameters:

    Returns:
        This is the report that will be saved into the secondary reports folder.
------------------------------------------------------------------------------------------------------------------------
7. consolidate_and_index_report():
        Function:
            This function will merge all the individual reports in the elementary and secondary report folders separately
            and index them in their respective files.

            Parameters:

        Returns:
            The 2 final CEO Review Reports that will be extracted as excel files.
========================================================================================================================
"""

# For testing
if __name__ == "__main__":
    """
    Testing get_ceo_report_raw_data
    """
    # Declare a report configuration
    report_config = {
        "report_name": "cwsn",
        "report_code" : "CWSN",
        "report_desc": "CWSN CEO report",
        "generate_report": True,
        "source_config" : {
            "source_file_name" : "CWSN-Report.xlsx",
            "source_sheet_name" : "Report",
            "skip_rows" : 4
        },
        "pre_process_brc_merge": True,
        "brc_merge_config" : {
            "join_on" : ["cols.district_name", "cols.block_name", "cols.school_name", "cols.school_category", "cols.udise_col"],
            "merge_type" : "left"
        },
        "post_process_brc_merge" : False,
    }

    get_ceo_report(report_config, 'Elementary', 'UNRANKED')
    

    #merged_data = get_ceo_report_raw_data(report_config)

    #file_utilities.save_to_excel({'Merged data' : merged_data}, 'Merged Data.xlsx')