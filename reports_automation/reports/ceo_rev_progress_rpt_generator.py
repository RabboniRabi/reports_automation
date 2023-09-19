"""
Module with functions to generate progress reports with visual
indicators to highlight improvement/decrease in performance between
current and previous reports
"""

import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities
import utilities.column_names_utilities as cols

from enums.school_levels import SchoolLevels as school_levels

def generate_ceo_rev_deo_progress_report(deo_lvl: school_levels):
    """
    Function to generate a progress report for DEOs
    based on improvement/decrease in ranks for each metric compared
    between current month and previous month.

    Parameters:
    -----------
    deo_lvl:school_levels
        school_levels enum value indicating if report needs to be generated for 
        Elementary or Secondary DEOs

    """
    
    # Get the current month data 
    curr_month = utilities.get_curr_month()
    curr_year = utilities.get_curr_year()
    df_curr_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [deo_lvl.value], [curr_month], [curr_year])

    # Get the data in progress report format
    df_curr_month_rpt = _build_progress_report(df_curr_month_ranks)
    

    # Get the previous month data
    prev_month = utilities.get_prev_month()
    prev_month_year = utilities.get_year_of_prev_month()
    df_prev_month_ranks = ranking_utilities.get_ceo_rev_ranking_master_data(\
                                ['DEO'], [schl_lvl], [prev_month], [prev_month_year])

    
    # Get the data in progress report format
    df_prev_month_progress_rpt = _build_progress_report(df_prev_month_ranks)


    # Subtract the previous month ranks
    df_improvement = df_curr_month_rpt.sub(df_prev_month_progress_rpt, fill_value=0)

    # Merge the current month 
    df_curr_month_progress_rpt = _merge_data_with_improv_data(df_curr_month_rpt, \
                    df_improvement, [cols.name, cols.desig, cols.school_level])

    # testing
    file_utilities.save_to_excel({'test': df_curr_month_progress_rpt}, 'df_curr_month_progress_rpt.xlsx')



    


def _build_progress_report(df_ranking_master):
    """
    Internal helper function to breakdown the ranking master and
    create a progress report where each 
    metric code is a column and the ranks people have received in that metric code
    are values.

    Parameters:
    ----------
    df_ranking_master: Pandas DataFrame
        The ranking master data

    Returns:
    -------
    Pandas DataFrame object of the the progress report
    """

    # Build the current month progress report - metric code column name: rank values
    # Get the metric codes for the month
    metric_codes = df_ranking_master[cols.metric_code].unique()

    # Iterate through the metric codes
    for metric_code in metric_codes:
        # Filter the data to the current metric code
        df_metric_code_filtered = utilities.filter_dataframe_column(\
                                    df_ranking_master, cols.metric_code, [metric_code])

        # Create a column with the metric code as column name and values as rank
        df_ranking_master[metric_code] = df_metric_code_filtered[cols.rank_col]

    # Fill the empty values with 0
    df_ranking_master.fillna(0, inplace=True)

    # Drop the columns containing all the ranks and metric codes
    df_ranking_master.drop(columns=[cols.rank_col, cols.metric_code, cols.ranking_value_desc], inplace=True)

    return df_ranking_master


def _merge_data_with_improv_data(df, df_improv, merge_on):
    """
    Internal helper function to merge the data with the improvement data.

    Parameters:
    ----------
    df: Pandas DataFrame
        Data with ranks for each metric code
    df_improv: Pandas DataFrame
        Data with improvement values in ranks for each metric code
    merge_on: list
        The list of columns to merge the data on
    Returns:
    ------
    Pandas DataFrame object of data merged with improvement data
    """

    # Append 'improv' string to the metric code column names
    metric_codes = df_improv[cols.metric_code].unique()
    rename_dict = {}
    for metric_code in metric_codes:
        rename_dict[metric_code] = metric_code + '_improvement'
    df_improv.rename(columns=rename_dict, inplace=True)

    # Merge the rank improvement values data with the current month ranks
    df_merged = df.merge(df_improv, how='left', on=merge_on)

    return df_merged

if __name__ == '__main__':

    # Generate the elementary DEOs progress report
    generate_ceo_rev_deo_progress_report(school_levels.ELEMENTARY)

