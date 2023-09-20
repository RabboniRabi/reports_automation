"""
Module with functions to fetch ranking weightages for report metrics
"""

import sys
sys.path.append('../')

import reader.config_reader as config_reader
from enums.school_levels import SchoolLevels as school_levels

def fetch_ceo_rev_metric_ranking_weightages(report_level:str=None):
    """
    Function to fetch the ranking weightage for 
    active metrics in ceo report configs for 
    elementary/secondary/ceo level

    Parameters:
    ----------
    report_level: str
        The level of the report to fetch the metrics for:
        Elementary/Secondary/None. Default is None. If none,
        the metrics are fetched at the report level (CEO).
        For elementary, the weightage is fetched from the 
        elementary config within the config. 
        Likewise for secondary.
    

    Returns:
    -------
    Dictionary of metric code key - weightages value pairs
    Eg: {
        "metric_code_1" : 0.5,
        "metric_code_2" : 0.4
        }
    """

    if report_level == school_levels.ELEMENTARY.value:
        config_level = 'elementary_report'
    elif:
        report_level == school_levels.SECONDARY.value:
        config_level = 'secondary_report'
    else:
        config_level = 'ceo'


    metric_weigtages_dict = {}

    # Get the CEO review configs
    ceo_review_configs = config_reader.get_all_active_ceo_review_configs()

    # Go through each active CEO review config and build the metric weightages dict
    for config in ceo_review_configs:
        
        metric_code = config['report_code']

        if config_level == 'ceo':

            metric_weigtages_dict[metric_code] = config['ranking_weightage']
        else:
            metric_weigtages_dict[metric_code] = config[config_level]['ranking_weightage']

    return metric_weigtages_dict


def fetch_ceo_rev_metric_improv_weightages(report_level:str=None):
    """
    Function to fetch the improvement weightage for 
    active metrics in ceo report configs for 
    elementary/secondary/ceo level

    Parameters:
    ----------
    report_level: str
        The level of the report to fetch the metrics for:
        Elementary/Secondary/None. Default is None. If none,
        the metrics are fetched at the report level (CEO).
        For elementary, the weightage is fetched from the 
        elementary config within the config. 
        Likewise for secondary.
    

    Returns:
    -------
    Dictionary of metric code key - weightages value pairs
    Eg: {
        "metric_code_1" : 0.5,
        "metric_code_2" : 0.4
        }
    """

    if report_level == school_levels.ELEMENTARY.value:
        config_level = 'elementary_report'
    elif:
        report_level == school_levels.SECONDARY.value:
        config_level = 'secondary_report'
    else:
        config_level = 'ceo'


    metric_weigtages_dict = {}

    # Get the CEO review configs
    ceo_review_configs = config_reader.get_all_active_ceo_review_configs()

    # Go through each active CEO review config and build the metric weightages dict
    for config in ceo_review_configs:
        
        metric_code = config['report_code']

        if config_level == 'ceo':

            metric_weigtages_dict[metric_code] = config['improvement_weightage']
        else:
            metric_weigtages_dict[metric_code] = config[config_level]['improvement_weightage']

    return metric_weigtages_dict