"""
Module with custom functions to create potential dropout students report.
"""

import sys

sys.path.append('../')

import pandas as pd

import utilities.column_names_utilities as cols

import utilities.dbutilities as dbutilities

# Define elementary indexes for pivoting
grouping_level = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name]


def pre_process_BRC_merge(raw_data: pd.DataFrame):
    """
    Function to process the potential dropouts raw data before merging with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data: Pandas DataFrame
        The raw potential dropouts

    Returns:
    -------
    DataFrame object of potential dropouts data processed and ready for mapping with BRC-CRC data
    """

    raw_data = raw_data[raw_data[cols.school_type] == 'Government']

    # Get school level class wise count of potential dropout students
    df_pivot_class_wise = pd.pivot_table(raw_data, values=cols.emis_id, index=grouping_level,
                                         columns=[cols.class_number],
                                         aggfunc='count', fill_value=0).reset_index()


    # Convert all column name types to string
    df_pivot_class_wise.columns = df_pivot_class_wise.columns.map(str)

    df_tot_pot_dropouts_schl = raw_data.groupby(grouping_level).agg({cols.emis_id: 'count'})

    # Rename the emis_id column to a more appropriate name
    df_tot_pot_dropouts_schl.rename(columns={
        cols.emis_id:cols.oosc_pot_dropout_count}, inplace=True)

    # Fetch the school level total students class 1-12 count in order to calculate potential dropout percent
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')
    df_class_1_12_tot_count = dbutilities.fetch_data_as_df(credentials_dict,
                                                           'class_1-12_government_aided_school_count.sql')

    # Merge the total potential dropout count to the class wise count
    df_merged = pd.merge(df_class_1_12_tot_count, df_pivot_class_wise, on=grouping_level)
    df_merged = pd.merge(df_merged, df_tot_pot_dropouts_schl, on=grouping_level)


    return df_merged
