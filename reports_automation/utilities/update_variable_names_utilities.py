"""
Module with utility functions related to updating variable names that are configured in JSON
and do not automatically resolve to the variable name value.
"""
import sys
sys.path.append('../')
import utilities.column_names_utilities as cols
from enums.ranking_types import RankingTypes as ranking_types

def update_ranking_args_dict(ranking_args:dict):
    """
    Utility function to update the ranking arguments read from the JSON configuration.
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

    # Update the boolean values for sorting and ascending flags
    ranking_args['sort'] = ranking_args['sort'] == 'True'
    ranking_args['ascending'] = ranking_args['ascending'] == 'True'

    ranking_type = ranking_args['ranking_type']

    if ranking_type == ranking_types.PERCENT_RANKING.value:
        # Update the numerator and denominator columns
        num_col_val = cols.get_value(ranking_args['num_col'])
        ranking_args['num_col'] = num_col_val
        den_col_val = cols.get_value(ranking_args['den_col'])
        ranking_args['den_col'] = den_col_val

    if ranking_type == ranking_types.MULT_COLS_PERCENT_RANKING.value:
        # Update the numerator and denominator columns
        num_col_val = cols.get_values(ranking_args['num_col'])
        ranking_args['num_col'] = num_col_val
        den_col_val = cols.get_values(ranking_args['den_col'])
        ranking_args['den_col'] = den_col_val
    
    if ranking_type == ranking_types.AVERAGE_RANKING.value:
        # Update the list of columns to average on
        updated_list = cols.get_values(ranking_args['avg_cols'])
        ranking_args['avg_cols'] = updated_list

    if ranking_type == ranking_types.NUMBER_RANKING.value:
        ranking_col = cols.get_value(ranking_args['ranking_col'])
        ranking_args['ranking_col'] = ranking_col

    return ranking_args


def update_ad_hoc_config_dict(report_config: dict):
    """
    Utility function to update the report configuration read from the JSON configuration.
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
    merge_sources_configs = report_config['merge_sources_configs']
    for merge_source_config_name in merge_sources_configs.keys():
        # Update the list of columns to join on
        updated_list = cols.get_values(merge_sources_configs[merge_source_config_name]['join_on'])
        merge_sources_configs[merge_source_config_name]['join_on'] = updated_list

    # Update the variable name strings in the summary sheets arguments
    for summary_sheet_arg in report_config['summary_sheets_args']:
        # Update the list of columns to group the data on
        updated_list = cols.get_values(summary_sheet_arg['grouping_levels'])
        summary_sheet_arg['grouping_levels'] = updated_list

        # Update the keys in the summary sheet aggregation dict to resolve string variable names
        updated_summary_args_dict = cols.update_dictionary_var_strs(summary_sheet_arg['agg_dict'])
        summary_sheet_arg['agg_dict'] = updated_summary_args_dict

        # Update the ranking arguments
        ranking_args = summary_sheet_arg['ranking_args']
        ranking_args = update_ranking_args_dict(ranking_args)

    return report_config
        

def update_ceo_review_config_dict(report_config: dict):
    """
    Utility function to update the CEO review report configuration read from the JSON configuration.
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

    # Update the configs by replacing variable string names with corresponding values

    brc_merge_config = report_config['brc_merge_config']
        
    join_on_vars = brc_merge_config['join_on']
    brc_merge_config['join_on'] = cols.get_values(join_on_vars)

    # Update the 'join_on' variable names if combine_sources_configs is given
    if 'combine_data_configs' in report_config and bool(report_config['combine_data_configs']):
        for key in report_config['combine_data_configs'].keys():
            combine_config = report_config['combine_data_configs'][key]
            if 'join_on' in combine_config:
                combine_config['join_on'] = cols.get_values(combine_config['join_on'])

    if 'elementary_report' in report_config and bool(report_config['elementary_report']):
        elem_report_config = report_config['elementary_report']
        # Get the arguments for generating elementary unranked report
        un_ranked_report_config  = elem_report_config['un_ranked_report_args']

        # Get the columns to group by
        grouping_cols = un_ranked_report_config['grouping_cols']
        # Update the values of column names to group by (To resolve string variable names).
        un_ranked_report_config['grouping_cols'] = cols.get_values(grouping_cols)

        # Get the aggregate functions to apply on the grouped columns
        agg_dict = un_ranked_report_config['grouping_agg_dict']
        # Update the keys in the aggregate dictionary as the string variable
        # names will not be resolved after being read from JSON
        un_ranked_report_config['grouping_agg_dict'] = cols.update_dictionary_var_strs(agg_dict)

        # Update the ranking arguments
        ranking_args = elem_report_config['ranking_args']
        elem_report_config['ranking_args'] = update_ranking_args_dict(ranking_args)

    if 'secondary_report' in report_config and bool(report_config['secondary_report']):
        sec_report_config = report_config['secondary_report']
        # Get the arguments for generating elementary unranked report
        un_ranked_report_config  = sec_report_config['un_ranked_report_args']

        # Get the columns to group by
        grouping_cols = un_ranked_report_config['grouping_cols']
        # Update the values of column names to group by (To resolve string variable names).
        un_ranked_report_config['grouping_cols'] = cols.get_values(grouping_cols)

        # Get the aggregate functions to apply on the grouped columns
        agg_dict = un_ranked_report_config['grouping_agg_dict']
        # Update the keys in the aggregate dictionary as the string variable
        # names will not be resolved after being read from JSON
        un_ranked_report_config['grouping_agg_dict'] = cols.update_dictionary_var_strs(agg_dict)

        # Update the ranking arguments
        ranking_args = sec_report_config['ranking_args']
        sec_report_config['ranking_args'] = update_ranking_args_dict(ranking_args)

    

