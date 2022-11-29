"""
Sample code to demonstrate utilization of ranking functionality
"""

import sys
sys.path.append('../')

import ceo_reports.ranking as ranking
import pandas as pd

def main():

    df_ranking = pd.DataFrame({
        
                    'District': ['Tiruvanamalai', 'Chennai', 'Villupuram'],

                   'Block': ['block 1', 'block 21', 'block 33'],

                   'Name': ['xyz', 'abc', 'ijk'],

                   'Designation': ['DEO', 'DEO', 'DEO'],
                   
                   'class_1': [10, 23, 17],

                   'Total': [100, 140, 34]
                   
                   })

    # Define a dictionary of arguments to calculate ranking
    ranking_args_dict = {
        'group_levels' : ['District', 'Name', 'Designation'],
        'agg_cols' : ['class_1', 'Total'],
        'agg_func' : 'sum',
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : True, 
        'ascending' : False
    }

    df_ranked = ranking.calc_ranking(df_ranking, 'percent_ranking',  ranking_args_dict)

    print('df_ranked: ', df_ranked)

    ranking.update_ranking_master(df_ranked, 'CP', 'Enrollment', 'Elementary')               



if __name__ == "__main__":
    main()
