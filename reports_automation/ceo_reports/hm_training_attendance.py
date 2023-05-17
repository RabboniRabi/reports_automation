"""

"""

import sys
sys.path.append('../')
import pandas as pd
import os
import utilities.column_names_utilities as cols
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import data_cleaning.column_cleaner as column_cleaner

grouping_levels = [cols.district_name, cols.block_name, cols.udise_col]
def get_mapping_data():

    # Block Information Source data
    block_data_file_name = "Sch-Enrollment-Abstract.xlsx"
    block_data_sheet_name = "Report"
    mapping_data_dir = file_utilities.get_mapping_data_dir_path()
    # read from excel, get sub columns
    mapping_file_path = os.path.join(mapping_data_dir, block_data_file_name)
    source_data = pd.read_excel(mapping_file_path, sheet_name=block_data_sheet_name)
    # Rename the column names to standard format
    column_cleaner.standardise_column_names(source_data)

    return source_data

def pre_process_BRC_merge(raw_data):
    """
       Function to process the HM training raw data before merging with BRC-CRC mapping data

       Parameters:
       ----------
       raw_data: Pandas DataFrame
           The raw hm training attendance raw data

       Returns:
       -------
       DataFrame object of HM training raw data processed and ready for mapping with BRC-CRC data
       """

    print('Pre Processing before BRC merge called in HM Training Attendance report')
    # Getting Block Level information
    source_data = get_mapping_data()
    raw_data[cols.block_name] = raw_data[cols.udise_col].apply(utilities.xlookup, args=(source_data[cols.udise_col], source_data[cols.block_name], False))
    # Getting Attendance Summary
    df_pivot = pd.pivot_table(raw_data, values=cols.school_name, index=grouping_levels,
                              columns=cols.attendance, aggfunc='count', fill_value=0).reset_index()
    # Finding out total invited from present, absent, absent&replaced and not filled
    df_pivot[cols.total_invited] = df_pivot[cols.present] + df_pivot[cols.absent] + df_pivot[cols.absent_replaced] + df_pivot[cols.not_filled]
    df_pivot.fillna(0)

    return df_pivot




