"""
Module with functions to fetch reports given report codes/names.

This module can be paired with a constructor in the future to create APIs to these functions.
"""

import config_reader
import ceo_report_generator


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


# For testing
if __name__ == "__main__":
    """
    Testing get_ceo_report_raw_data
    """
    merged_data = get_ceo_report_raw_data('cwsn')

    print('merged data columns: ', merged_data.columns.to_list())