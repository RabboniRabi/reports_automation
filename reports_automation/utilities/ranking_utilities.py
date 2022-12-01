"""
Module with utilitiy functions to calculate and save ranking
"""

import os
import sys
sys.path.append('../')
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.ranking_funcs_utilities as ranking_funcs_utilities
import utilities.column_names_utilities as cols

import pandas as pd
from datetime import datetime



# Name of the master report with all the rankings
ranking_master_file_name = 'ranking_master.xlsx'
ranking_master_sheet_name = 'ranking'
# Get the path to the ceo_reports folder for the month
ceo_rpts_dir_path = file_utilities.get_ceo_rpts_dir_path()


# Define the columns to save to the ranking master
cols_to_save = [cols.district, cols.name, cols.desig, cols.rank_col, cols.ranking_value, cols.ranking_value_desc,\
    cols.metric_code, cols.metric_category, cols.school_level, cols.month_col, cols.year_col]



def calc_ranking(df, group_cols, ranking_type, ranking_args_dict):
    """
    Function to calculate ranking for data based on the type of ranking given.
    The function uses the dictionary in ranking_utilities to match the ranking type and 
    calls the appropriate ranking function which will calculate and return the rank.

    Paramters:
    ----------
    df: Pandas DataFrame
        The data to be ranked
    group_levels: list
        The list of columns to group by
    ranking_type: str
        The type of ranking to be used to calculate the ranking for the data
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_cols' : ['class_1', 'Total'],
        'agg_func' : 'sum',
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : True,
        'ascending' : False
        }
    Returns:
    --------
    Ranked DataFrame object
    """
    ranking_func = ranking_funcs_utilities.get_ranking_funcs().get(ranking_type)
    
    return ranking_func(df, group_cols, ranking_args_dict)



def update_ranking_master(df_ranking, metric_code, metric_category, school_level):
    """
    Function to update the master ranking file with the given ranking data for the current month.

    The ranking master file is stored in the ceo_reports folder in generated reports.
    
    Parameters:
    -----------
    df_ranking: Pandas DataFrame
        The ranked data for a metric
    metric_code: str
        The code for the metric used in the calculation of the ranking
    metric_category: str
        The category the ranked metric falls under
    school_level: str
        The level of school education the ranking is for: Elementary or Secondary    
    """

    # Update the ranking data with columns indicating metrics, school level and month-year
    df_ranking[cols.metric_code] = metric_code
    df_ranking[cols.metric_category] = metric_category
    df_ranking[cols.school_level] = school_level
    df_ranking[cols.month_col] =  datetime.now().strftime('%h')
    df_ranking[cols.year_col] =  int(datetime.now().strftime('%Y'))
    
    # Get the master ranking file. In the future, this needs to be saved and fetched from a database
    ranking_file_path = os.path.join(ceo_rpts_dir_path, ranking_master_file_name)

    # If file does not exist, save the ranking to the file
    if not os.path.exists(ranking_file_path):
        df_master_ranking = df_ranking
    else:

        # Get the master ranking file
        df_master_ranking = pd.read_excel(ranking_file_path, ranking_master_sheet_name)

        # Define the subset of columns to check for common rows
        cols_to_check = [cols.district, cols.name, cols.desig, cols.metric_code, cols.school_level, cols.month_col, cols.year_col]

        # Check if ranking data already exists
        if (utilities.is_any_row_common(df_master_ranking[cols_to_check], df_ranking[cols_to_check])):
            # Then update with the latest ranking
            df_master_ranking.update(df_ranking)
        else:
            # Add the new ranking to the ranking master
            df_master_ranking = pd.concat([df_master_ranking, df_ranking], join='inner')

    # Get only the columns to save.
    df_master_ranking = df_master_ranking[cols_to_save]        

    # Save the updated df_master_ranking
    df_sheet_dict = {ranking_master_sheet_name: df_master_ranking}
    file_utilities.save_to_excel(df_sheet_dict, ranking_master_file_name, ceo_rpts_dir_path)
