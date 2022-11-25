"""
Module with functions to calculate and save ranking
"""

import os
import sys
sys.path.append('../')
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.ranking_utilities as ranking_utilities

import pandas as pd
from datetime import datetime



# Name of the master report with all the rankings
ranking_master_file_name = 'ranking_master.xlsx'
ranking_master_sheet_name = 'ranking'
# Get the path to the ceo_reports folder for the month
ceo_rpts_dir_path = file_utilities.get_ceo_rpts_dir_path()


# Get and update ranking
#def get_and_update_ranking(df_data, metric_code, metric_category, school_level):
    


def update_ranking_master(df_ranking, metric_code, metric_category, school_level):
    """
    Function to update the master ranking file  with the given ranking data for the current month
    
    Parameters:
    -----------
    df_ranking: Pandas DataFrame
        The calculated ranking data for a metric
    metric_code: str
        The code for the metric used in the calculation of the ranking
    metric_category: str
        The category the ranked metric falls under
    school_level: str
        The level of school education the ranking is for: Elementary or Secondary    

    """

    # Update the ranking data with columns indicating metrics, school level and month-year
    df_ranking['metric_code'] = metric_code
    df_ranking['metric_category'] = metric_category
    df_ranking['school_level'] = school_level
    df_ranking['Month'] =  datetime.now().strftime('%h')
    df_ranking['Year'] =  datetime.now().strftime('%y')
    
    # Get the master ranking file. In the future, this needs to be saved and fetched from a database
    ranking_file_path = os.path.join(ceo_rpts_dir_path, ranking_master_file_name)

    # If file does not exist, save the ranking to the file
    if not os.path.exists(ranking_file_path):
        df_master_ranking = df_ranking
    else:

        # Get the master ranking file
        df_master_ranking = pd.read_excel(ranking_file_path, ranking_master_sheet_name)

        # Define the subset of columns to check for common rows
        cols_to_check = ['District', 'Block', 'Name', 'metric_code', 'school_level', 'Month', 'Year']

        # Check if ranking data already exists
        if (utilities.is_any_row_common(df_master_ranking[cols_to_check], df_ranking[cols_to_check])):
            # Then update with the latest ranking
            df_master_ranking.update(df_ranking)
        else:
            # Add the new ranking to the ranking master
            df_master_ranking = pd.concat([df_master_ranking, df_ranking], join='inner')

    # Save the updated df_master_ranking
    df_sheet_dict = {ranking_master_sheet_name: df_master_ranking}
    file_utilities.save_to_excel(df_sheet_dict, ranking_master_file_name, ceo_rpts_dir_path)

    

def main():
    """
    For testing
    """
    df_ranking = pd.DataFrame({'District': ['Tiruvanamalai', 'Chennadi', 'Villupuram'],

                   'Block': ['block 1', 'block 21', 'block 33'],
                   
                   'Name': ['Ram', 'Rahim', 'Robert'],

                   'Rank': [1, 2, 3]
                   
                   })
    #update_ranking_master(df_ranking, 'CP', 'Enrollment', 'Elementary')


    percent_ranking_args = [ ['A', 'B'], ['C'], 'sum', 'frac_col', 'numerator', 'denominator', 'rank']
    ranking_utilities.calc_ranking('percent_ranking', df_ranking,  percent_ranking_args)
    


if __name__ == "__main__":
    main()
