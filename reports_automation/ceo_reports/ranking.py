"""
Module with functions to calculate and save ranking
"""
import os
import sys
sys.path.append('../')
import utilities.file_utilities as file_utilities


# Name of the master report with all the rankings
ranking_master_file_name = 'ranking_master.xlsx'
# Get the path to the ceo_reports folder inside the generated reports folder
ranking_file_path = str(os.path.join(file_utilities.get_gen_reports_dir_path(), 'ceo_reports'))


# get ranking 


def update_ranking_master(df_ranking, metric):
    """
    Function to update the sheet for the current month in the master ranking file 
    with the given ranking data
    
    Parameters:
    -----------
    df_ranking: Pandas DataFrame
        The calculated ranking data for a metric
    metric: str
        The metric used in the calculation of the ranking    

    """

