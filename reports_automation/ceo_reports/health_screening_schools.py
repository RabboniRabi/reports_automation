import sys
sys.path.append('../')

import utilities.column_names_utilities as cols

def _get_data_with_school_level_scrn_status(df):
    """
    Internal function to update the data with school level
    Fully completed, Partially Completed, 'Not Started' screening statuses.

    Parameters:
    -----------
    df: Pandas DataFrame
        The health data to be updated with screening statuses of schools

    Returns:
    -------
    DataFrame object of data updated with schools screening statuses
    """
    # Compute whether a school has completed screening, partially completed or not started
    series_completed = (df[cols.total] - df[cols.screened] <= 0 ) & (df[cols.total]  != 0)
    series_not_started =  df[cols.screened] == 0
    series_partially_completed =  ~(series_completed | series_not_started)
    school_col_index = df.columns.get_loc(cols.school_name)            
    # Insert the computed values as series into the dataframe next to the school column
    df.insert(school_col_index+1,cols.fully_comp, series_completed)
    df.insert(school_col_index+2,cols.part_comp, series_partially_completed)
    df.insert(school_col_index+3,cols.not_started, series_not_started)


    return df

def post_process_BRC_merge(raw_data_brc_merged):
    """
    Function to process the Heatlh raw data after being merged with BRC-CRC mapping data

    Parameters:
    ----------
    raw_data_brc_merged: Pandas DataFrame
        The raw Health screening data merged with BRC-CRC mapping data

    Returns:
    -------
    DataFrame object of Health screening data ready for report generation
    """

    print('post process called for health screening schools')

    df_data = _get_data_with_school_level_scrn_status(raw_data_brc_merged)

    return df_data