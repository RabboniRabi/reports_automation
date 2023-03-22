"""
Module with function for custom pre-processing of Library book assigning report
"""


import sys
sys.path.append('../')

import utilities.column_names_utilities as cols

import pandas as pd

# Define the initial grouping level
initial_group_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name, cols.school_category]


def pre_process_BRC_merge(raw_data):
    """
    Function to process the Library raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw Library book assigining data

    Returns:
    -------
    DataFrame object of library book assigning data processed and ready for mapping with BRC-CRC data
    """

    print('Pre Processing before BRC merge called in Library book assigning by teachers report')

    df_pivot = pd.pivot_table(raw_data, values=cols.section,\
                        index = initial_group_levels, columns=[cols.book_assigning_status], aggfunc='count',fill_value=0).reset_index()

    # Rename the books assigned columns for appropriate readability
    df_pivot.rename(columns={
        cols.books_assigned : cols.sctns_assigning_books,
        cols.books_not_assigned: cols.sctns_not_assigning_books}, inplace=True)

    df_pivot[cols.tot_sections] = df_pivot[cols.sctns_assigning_books] + df_pivot[cols.sctns_not_assigning_books]


    return df_pivot
