import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities

import utilities.column_names_utilities as cols
import pandas as pd
import numpy as np

# Get the reason type column
reason_type_col = cols.reason_type


def _get_reason_type_summary(df, grouping_level):
    """
    Internal function to get the reason type-grouping level wise summary
    of OSC data.

    Parameters:
    -----------
    df: DataFrame
        The raw OSC data
    grouping_level: list
        The list of levels to group the data by
    """

    # Clean the reason type values
    #to_be_admitted_vals = df[reason_type_col] == '"To be Admitted"' or 'To be admitted'
    #df_admitted_vals = df[df[reason_type_col] == '"To be Admitted"' or 'To be admitted']
    df[reason_type_col].replace(to_replace=['To be admitted', 'To be Admitted '] , value='To be Admitted', inplace=True)



    # Get reason type wise summary of OSC data
    df_pivot = pd.pivot_table(df, values=cols.student_name, \
                        index=grouping_level ,columns=[reason_type_col], aggfunc='count',fill_value=0).reset_index()

    return df_pivot


def run():
    """
    Main function that calls other internal functions to generate the report
    """

    file_path = file_utilities.get_curr_month_source_data_dir_path() + '/OSC-Survey-Full-Rpt.xlsx'
    df_report = pd.read_excel(file_path, sheet_name='Report',skiprows=4)

    # Define the levels to group the data by
    grouping_levels = [cols.district_name]
    df_reason_type_summ = _get_reason_type_summary(df_report, grouping_levels)

    file_utilities.save_to_excel({'Report':df_reason_type_summ}, 'OoSC_test.xlsx')

if __name__ == "__main__":
    run()