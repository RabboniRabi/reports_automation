"""
Module with functions to fetch reports given report codes/names.

This module can be paired with a constructor in the future to create APIs to these functions.
"""
import sys
sys.path.append('../')

import readers.config_reader as config_reader
import ceo_report_generator
import ad_hoc_report_generator



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


def generate_ad_hoc_report(report_code, save_source=False, save_report=False):
    """
    Function to generate & fetch the ad hoc report for a given report code/name. 

    Parameters:
    ----------
    report_code: str
        The name/code of the report/metric to fetch the Ad Hoc report for
    save_source: bool
        Flag indicating if a copy of data fetched from database needs to be saved.
        To be used within the application. Default is False.
    save_report: bool
        Flag indicating if report needs to be saved. Default is False

    Returns:
    -------
    The generated report for the given report code
    """

    # Get the overall configuration for the report code
    report_config = config_reader.get_adhoc_config(report_code)

    # Get the ad hoc report
    ad_hoc_rpt = ad_hoc_report_generator.get_report(report_config, save_report)

    if save_report:
        report_name = report_config['report_name']
        ad_hoc_report_generator.save_report(report_name, ad_hoc_rpt)

    return ad_hoc_rpt


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
    """elem_report = get_ceo_report('TCH_ATT_MARK', 'Elementary', 'Ranked')
    file_utilities.save_to_excel({'Report': elem_report}, 'TCH_ATT_MARK Elementary Report.xlsx')

    sec_report = get_ceo_report('TCH_ATT_MARK', 'Secondary', 'Ranked')
    file_utilities.save_to_excel({'Report': sec_report}, 'TCH_ATT_MARK Secondary Report.xlsx')"""


    """
    Testing get_ad_hoc_report
    """

    adhoc_report = get_ad_hoc_report('teacher_leave_absence_update')
    dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
    file_utilities.save_to_excel({'Report': adhoc_report}, 'teacher_leave_absence_update.xlsx', dir_path)



    