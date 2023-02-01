"""
Module with functions to fetch reports given report codes/names.

This module can be paired with a constructor in the future to create APIs to these functions.
"""

import config_reader
import ceo_report_generator

import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities

def get_ceo_report_raw_data (report_code):
    """
    Function to fetch the raw data for CEO reports. This data would be
    the raw data processed and merged with BRC-CRC mapping data.

    Parameters:
    -----------
    report_code: str
        The name/code of the report/metric to fetch the CEO report format raw data for

    Returns:
    --------
    CEO report format raw data as a DataFrame object.
    """

    # Get the overall configuration for the report
    report_config = config_reader.get_config(report_code)

    # Get the CEO Report format raw data for the given report
    ceo_rpt_raw_data = ceo_report_generator.get_ceo_report_raw_data(report_config)

    return ceo_rpt_raw_data


def get_ceo_report(report_code, school_level, report_level):
    """
    Function to generate & fetch the CEO report for a given report code/name. 

    The report can be generated for Elementary/Secondary school level and
    can be Ranked/Unranked report

    Parameters:
    ----------
    report_code: str
        The name/code of the report/metric to fetch the CEO report for
    school_level: str
        The school level to filter and generate the report for (Elementary/Secondary)
    report_level: str
        The level of report to be generated. (Unranked/Ranked)

    Returns:
    -------
    The generated report for the given report code
    """

    # Get the overall configuration for the report code
    report_config = config_reader.get_config(report_code)

    # Get the CEO report
    ceo_rpt = ceo_report_generator.get_ceo_report(report_config, school_level, report_level)

    return ceo_rpt



# For testing
if __name__ == "__main__":
    """
    Testing get_ceo_report_raw_data
    """
    #merged_data = get_ceo_report_raw_data('cwsn')

    #print('merged data columns: ', merged_data.columns.to_list())

    """
    Testing get_ceo_report
    """
    elem_report = get_ceo_report('students_ageing_in_common_pool', 'Elementary', 'Ranked')
    file_utilities.save_to_excel({'Report': elem_report}, 'CP Elementary Report.xlsx')

    sec_report = get_ceo_report('CP', 'Secondary', 'Ranked')
    file_utilities.save_to_excel({'Report': sec_report}, 'CP Secondary Report.xlsx')

    

    