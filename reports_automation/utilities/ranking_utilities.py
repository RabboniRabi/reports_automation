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
from enums.school_levels import SchoolLevels as school_levels

import pandas as pd
from datetime import datetime



# Name of the master report with all the rankings
ranking_master_file_name = 'ranking_master.xlsx'
ranking_master_sheet_name = 'ranking'
# Get the path to the ceo_reports folder for the month
ranking_rpts_dir_path = file_utilities.get_ranking_reports_dir()


# Define the columns to save to the ranking master
cols_to_save = [cols.name, cols.desig, cols.rank_col, cols.ranking_value, cols.ranking_value_desc,\
    cols.metric_code, cols.metric_category, cols.school_level, cols.month_col, cols.year_col]

def calc_ranking(df, ranking_config):
    """
    Function to calculate ranking for data based on the ranking configuration given.

    The ranking configuration is designed to be flexible to perform different types
    of ranking on the data. 
    
    Values upon which the data is to be ranked can be calculated based on arguments in
    the configuration or on a specified column. 

    Multiple ranks can be calculated for different grouping of data. 
    
    Ranks can also be given within groups in the data. For example, 7 blocks in district A
    and 4 blocks in district B can be ranked 1-7 and 1-4 respectively within the data.

    There are also flags(toggles) to show rank, ranking value, to sort data, to order data, etc.

    Depending on the ranking type specified (matching types declared in RankingTypes Enum),
    the ranking value and rank is calculated.

    Paramters:
    ----------
    df: Pandas DataFrame
        The data to be ranked
    ranking_config: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg:
            'ranking_config' : {
                'ranking_args': {
                    'ranking_type' : 'percent_ranking',
                    'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
                    'ranking_val_desc' : '% moved to CP',
                    'num_col' : 'class_1',
                    'den_col' : 'Total',
                    'sort' : true,
                    'ascending' : false,
                    '// Below configs are to be used' : '//if data is to be ranked directly without grouping',
                    '// Below configs are ignored' :  '//if data_ranking_levels config is present',
                    'show_rank_col' : true/false,
                    'rank_col_name' : 'to be given if show_rank_col is true',
                    'show_rank_val: : true/false,
                    'ranking_val_desc' : 'to be given if show_rank_val is true'
                }
                '//Below data ranking levels are optional' : '//To be used if data is to be grouped and ranked'
                'data_ranking_levels' : {
                    'deo_level' : {
                        'grouping_levels' : ['cols.deo_name'],
                        'show_rank_col' : true,
                        'rank_col_name' : 'cols.deo_elem_rank',
                        'show_rank_val' : false,
                        '//ranking_val_desc is not needed' : '//as show_rank_val flag is false
                    },
                    'block_level' : {
                        'grouping_levels' : ['cols.deo_name', 'cols.block_name'],
                        'show_rank_col': false,
                        '//rank_col_name is not needed' : '//as show_rank_col flag is false
                        'show_rank_val' : true,
                        'ranking_val_desc' : 'cols.perc_screened'
                        '// or above two lines can be replaced with' : '//the following to do within group ranking',
                        'show_rank_col' : true,
                        'rank_col_name' : 'block_rank',
                        'rank_within_parent_group': true,
                        'rank_within_parent_grouping_levels' : ['cols.deo_name_elm']
                    }
                }
            } 
        
        
    Returns:
    --------
    Ranked DataFrame object
    """

    # Check if data has to be grouped and ranked
    if 'data_ranking_levels' in ranking_config:
        # Make a copy of the data to use for merging different levels of ranked data with original data
        df_ranked = df.copy()
        # Declare show rank column and show rank value flags
        show_rank_col_flag, show_rank_val_flag = False, False

        # For each grouping and ranking, call the ranking type specific function to rank the data
        # with updated ranking_args
        for key in ranking_config['data_ranking_levels']:

            grouping_lvl_ranking_config = ranking_config['data_ranking_levels'][key]
            
            # Get a copy of the ranking_args and update it for the current grouping and ranking
            ranking_args_for_key = ranking_config['ranking_args'].copy()
            
            if 'show_rank_col' in grouping_lvl_ranking_config and grouping_lvl_ranking_config['show_rank_col']:
                ranking_args_for_key['show_rank_col'] = grouping_lvl_ranking_config['show_rank_col']
                ranking_args_for_key['rank_col_name'] = grouping_lvl_ranking_config['rank_col_name']
                show_rank_col_flag = True
            
            if 'show_rank_val' in grouping_lvl_ranking_config and grouping_lvl_ranking_config['show_rank_val']:
                ranking_args_for_key['show_rank_val'] = grouping_lvl_ranking_config['show_rank_val']
                ranking_args_for_key['ranking_val_desc'] = grouping_lvl_ranking_config['ranking_val_desc']
                show_rank_val_flag = True
            
            if 'rank_within_parent_group' in grouping_lvl_ranking_config and grouping_lvl_ranking_config['rank_within_parent_group']:
                ranking_args_for_key['rank_within_parent_group'] = grouping_lvl_ranking_config['rank_within_parent_group']
                ranking_args_for_key['rank_within_parent_grouping_levels'] = grouping_lvl_ranking_config['rank_within_parent_grouping_levels']

            # Group the data to the level it needs to be ranked on
            grouping_levels = grouping_lvl_ranking_config['grouping_levels']
            df_grouped = df.groupby(grouping_levels, as_index=False, sort=False).agg(ranking_args_for_key['agg_dict'])

            # Call the ranking_type specific ranking function
            ranking_type = ranking_args_for_key['ranking_type']
            ranking_func = ranking_funcs_utilities.get_ranking_funcs().get(ranking_type)
            
            data_ranked_for_grouping_lvl = ranking_func(df_grouped, ranking_args_for_key)

            # Merge the rank and rank values, depending on which flags are true
            if show_rank_col_flag and show_rank_val_flag:
                # Get the subset of data with grouping levels and rank column and rank value column
                df_subset = data_ranked_for_grouping_lvl[grouping_levels + \
                            [grouping_lvl_ranking_config['rank_col_name'], grouping_lvl_ranking_config['ranking_val_desc']]]
            elif show_rank_col_flag:
                            # Get the subset of data with grouping levels and rank column and rank value column
                df_subset = data_ranked_for_grouping_lvl[grouping_levels + [grouping_lvl_ranking_config['rank_col_name']]]
            elif show_rank_val_flag:
                            # Get the subset of data with grouping levels and rank column and rank value column
                df_subset = data_ranked_for_grouping_lvl[grouping_levels + [grouping_lvl_ranking_config['ranking_val_desc']]]
            else:
                # No source configuration was found
                sys.exit('Atleast one of show_rank_col or show_rank_val flags need to be true')

            # Merge the ranked data for the current grouping level with the consolidated ranked data    
            df_ranked = pd.merge(df_ranked, df_subset, how='left', on=grouping_levels)
            # Reset the flags to false for next iteration
            show_rank_col_flag, show_rank_val_flag = False, False

    else:
        # Call the ranking_type specific ranking function 
        ranking_args = ranking_config['ranking_args']

        ranking_type = ranking_args['ranking_type']
        ranking_func = ranking_funcs_utilities.get_ranking_funcs().get(ranking_type)
            
        df_ranked = ranking_func(df, ranking_args)

    return df_ranked

def calc_ranking_old(df, ranking_args_dict):
    """
    Function to calculate ranking for data based on the type of ranking given.
    The function uses the dictionary in ranking_utilities to match the ranking type and 
    calls the appropriate ranking function which will calculate and return the rank.

    Paramters:
    ----------
    df: Pandas DataFrame
        The data to be ranked
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
                'ranking_type' : 'percent_ranking',
                'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
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
    ranking_type = ranking_args_dict['ranking_type']
    ranking_func = ranking_funcs_utilities.get_ranking_funcs().get(ranking_type)
    
    return ranking_func(df, ranking_args_dict)



def update_deo_ranking_master(df_ranking, metric_code, metric_category, school_level, ranking_val_desc):
    """
    Function to update the DEOs master ranking file with the given ranking data for the current month.

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
    ranking_val_desc: str
        Description string of ranking value
    """

    # Update the ranking data with columns indicating metrics, school level and month-year
    df_ranking[cols.metric_code] = metric_code
    df_ranking[cols.metric_category] = metric_category
    df_ranking[cols.school_level] = school_level
    df_ranking[cols.month_col] =  datetime.now().strftime('%h')
    df_ranking[cols.year_col] =  int(datetime.now().strftime('%Y'))
    df_ranking[cols.desig] = 'DEO'

    # Rename the DEO name rank column to generic name
    if school_level == school_levels.ELEMENTARY.value:
        df_ranking.rename(columns={cols.deo_name_elm: cols.name, cols.deo_elem_rank:cols.rank_col}, inplace = True)
    elif school_level == school_levels.SECONDARY.value:
        df_ranking.rename(columns={cols.deo_name_sec: cols.name, cols.deo_sec_rank:cols.rank_col}, inplace = True)

    # Add the ranking value description
    df_ranking[cols.ranking_value_desc] = ranking_val_desc

    # Rename the name of the column containing ranking value to generic 'Ranking Value' 
    df_ranking.rename(columns = {ranking_val_desc: cols.ranking_value}, inplace=True)

    # Convert all column types to string
    df_ranking = df_ranking.astype({
        cols.name: 'string',
        cols.desig: 'string',
        cols.metric_code : 'string',
        cols.metric_category: 'string',
        cols.school_level: 'string',
        cols.month_col: 'string',
        cols.year_col: 'int'})
    

    # If file does not exist, save the ranking to the file
    if not file_utilities.file_exists(ranking_master_file_name, ranking_rpts_dir_path):
        df_master_ranking = df_ranking
    else:

        # Get the master ranking file. In the future, this needs to be saved and fetched from a database
        ranking_file_path = file_utilities.get_file_path(ranking_master_file_name, ranking_rpts_dir_path)

        # Get the master ranking file
        df_master_ranking = pd.read_excel(ranking_file_path, ranking_master_sheet_name)

        # Define the subset of columns to check for common rows
        cols_to_check = [cols.name, cols.desig, cols.metric_code, cols.school_level, cols.month_col, cols.year_col]

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
    file_utilities.save_to_excel(df_sheet_dict, ranking_master_file_name, ranking_rpts_dir_path)



def rank_cols_insert(df, ranking_args_dict):
    """
    Function to sequentially sort and rank the data on 
    each of a given set of columns.
    
    For each of the columns, data is sorted and ranked in 
    ascending/descending order.

    The rank of the data based on each of the given columns 
    is inserted into the data. The location of where to insert
    the rank for the column can also be specified.

    The columns and their corresponding ranking variables like
    ascending/descending and other flags are to be provided as a dict.


    Parameters:
    -----------
    df: Pandas Data Frame
        Data to rank
    ranking_args_dict: dict
        For Example:
        "cols.curr_eng_marks": { # Column to rank on
            "insert_rank_col_name": "cols.eng_rank_state", # name of rank column
            "index_from_col": 1, # Position to insert the rank column from column
            "ascending": "False",
            "rank_frac" : "True",
                #True - If the rank be represented by rank/total number of records.
                #For Example: (15/175, 16/175...)
                #Default is False - Rank be represented as (1, 2 ,3...)
            "reset_sort" : "False" - Reset the sorted order of data by column
        }

    Returns:
    ------
    Ranked Dataframe
    """
    for sort_col, rank_args in ranking_args_dict.items():
        # Sort the dataframe based on the sort column
        df.sort_values(by=sort_col, ascending=rank_args['ascending'], inplace=True)
        # Calculate the index where the rank column needs to be inserted
        index_col = df.columns.get_loc(sort_col) + rank_args['index_from_col']
        # Insert the rank column and cell values 1,2,3 to length of data
        insert_rank_col_name = rank_args['insert_rank_col_name']
        df.insert(index_col, insert_rank_col_name, range(1, 1+len(df)))

        # Get total number of ranks
        total_ranks = len(df)

        if 'rank_frac' in rank_args and rank_args['rank_frac']:
            
            # Update the rank values as fraction of total rank: 1/100, 2/100, etc.
            df[rank_args['insert_rank_col_name']] = df[rank_args['insert_rank_col_name']]\
                        .apply(lambda rank: str(rank) + '/' + str(total_ranks))

    return df


def _group_data_for_ranking(df, groupong_levels:list, agg_dict:dict, sort:bool):
    """
    Helper function to group the data before it is ranked.
    Grouping is based on grouping levels and aggregate functions given in ranking arguments.

    In some scenarios, data might need to be grouped further before being ranked.
    Eg: Data at Block level, but needs to be ranked at DEO level.
    If no grouping related arguments are given, data is returned without grouping.

    Parameters:
    ----------
    df: Pandas DataFrame
        The data to be grouped before ranking
    ranking_args: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
            Eg: 
            "ranking_args" : {
                        "ranking_type" : "percent_ranking",
                        "ranking_group_level" : ["cols.district_name"],
                        "agg_dict": {
                            "cols.cg_clg_nm": "count", 
                            "cols.student_name" : "count"
                        },
                        "ranking_val_desc": "cols.cg_perc_stu_w_clg_name",
                        "num_col": "cols.cg_clg_nm",
                        "den_col": "cols.student_name",
                        "sort": "True",
                        "ascending": "False",
                        "show_rank_col" : "False"
                    }
    """

    ranking_group_level = ranking_args['ranking_group_level']
    agg_dict = ranking_args['agg_dict']
    sort = ranking_args_dict['sort']

    # If grouping level list and grouping aggregate dictionary is not empty
    if len(ranking_group_level) > 0 and agg_dict:
        # Group the data
        df_rank = df.groupby(ranking_group_level, as_index=False, sort=sort).agg(agg_dict)

def build_metric_wise_ranking_report(df_ranking_master):
    """
    Function to use the data in the ranking master format and
    create a ranking report where each metric code is 
    a column and the ranks people have received for that metric code
    are values.

    Parameters:
    ----------
    df_ranking_master: Pandas DataFrame
        The ranking master data

    Returns:
    -------
    Pandas DataFrame object of the the progress report
    """

    # Declare an empty DataFrame
    df_metric_wise_ranking = pd.DataFrame()
    
    # Get the metric codes in the given data
    metric_codes = df_ranking_master[cols.metric_code].unique()

    # Get the unique names in the given ranking master
    names = df_ranking_master[cols.name].unique()


    # Put the above names in the name column
    df_metric_wise_ranking[cols.name] = names


    # Iterate through the metric codes
    for metric_code in metric_codes:
        # Filter the data to the current metric code
        df_metric_code_filtered = utilities.filter_dataframe_column(\
                                    df_ranking_master.copy(), cols.metric_code, [metric_code])

        # Create a column with the metric code as column name and values as rank
        df_metric_code_filtered[metric_code] = df_metric_code_filtered[cols.rank_col]

        # Merge the metric code rank values to the metric wise ranking data
        df_metric_wise_ranking = pd.merge(df_metric_wise_ranking, \
                                    df_metric_code_filtered[[cols.name, metric_code]], on=[cols.name], how='left')

    # Sort the data alphabetically by names
    df_metric_wise_ranking.sort_values(by=cols.name)

    return df_metric_wise_ranking



def get_ceo_rev_ranking_master_data(designations: list, school_levels:list, months:list, years:list):
    """
    Function to get the CEO review ranking master data for given
    designation, school level, month and year

    Parameters:
    -----------
    designations: list
        The designations of the staff whose ranking details is to be fetched
    school_levels: list
        The school levels (Elementary/Secondary) for which the data is to be fetched
    months: list
        The months for which the data is to be fetched
    years: list 
        The years for which the data is to be fetched

    Returns:
    --------
    The ceo review ranking master data filtered for the given parameters
    """

    # Get the path to the ranking master
    ranking_rpts_dir_path = file_utilities.get_ranking_reports_dir()
    file_path = file_utilities.get_file_path('ranking_master.xlsx', ranking_rpts_dir_path)

    # Read the ranking master data as a Pandas DataFrame object
    df_ranking_master = file_utilities.read_sheet(file_path, 'ranking')

    # Get the ranking master data matching the given criteria
    df_filter_criteria = {}
    df_filter_criteria[cols.desig] = designations
    df_filter_criteria[cols.school_level] = school_levels
    df_filter_criteria[cols.month_col] = months
    df_filter_criteria[cols.year_col] = years

    df_ranking_master_filtered = utilities.filter_dataframe(df_ranking_master, df_filter_criteria)

    return df_ranking_master_filtered


def get_inverted_rank(df_ranking, metric_codes:list):
    """
    Function to invert the rank values in a report with
    column wise metric ranks.

    Parameters:
    -----------
    df_ranking: Pandas DataFrame
        The data whose metric wise ranking values are to be inverted
    metric_codes: list
        The list of metric code column names with ranking values
    """

    # Get the maximum ranks in the data
    max_rank = max(df_ranking[metric_codes[0]].unique())

    # Invert the ranks
    for metric_code in metric_codes:
        df_ranking[metric_code] = (max_rank + 1) - df_ranking[metric_code]

    return df_ranking


def compute_consolidated_ranking(df_ranking, metric_weightage:dict, invert_rank:bool=True):
    """
    Function to compute consolidated ranking for given metric wise rank values data

    Parameters:
    -----------
    df_ranking: Pandas DataFrame
        The data whose metric wise ranking values are to be used for consolidated ranking
    metric_weightage_dict: dict
        Dictionary of metric - weightage value key value pairs
    invert_rank: bool
        Flag indicating if rank values need to be inverted before it is multiplied with the weightage.
        For example, when using rank based weightage, rank values need to be inverted. i.e:
        higher ranks need to get more weightage. When using improvement based weightage, improvement values
        dont need to be inverted as more the improvement, higher the weightage value needs to be.

    Returns:
    --------
    Pandas DataFrame object of consolidated ranking from total of metric wise weightage
    """

    df_cons_ranking = df_ranking.copy()

    metric_codes = list(metric_weightage.keys())

    df_cons_ranking[cols.cons_tot_wt_scr] = 0

    # Check and invert the ranks if needed
    if invert_rank:
        df_cons_ranking = get_inverted_rank(df_cons_ranking, metric_codes)

    # For each metric
    for metric_code in metric_codes:
        # If weightage is zero, skip calculating weighted score for the metric
        if metric_weightage[metric_code] == 0:
            # Drop the column from consolidated ranking
            df_cons_ranking.drop(columns=[metric_code], inplace=True)
            continue
        
        # Calculate the weighted rank for the metric code
        df_cons_ranking[metric_code] = df_cons_ranking[metric_code] * metric_weightage[metric_code]

        # Fill NAs with 0s
        df_cons_ranking.fillna(0, inplace=True)

        # Update the total weighted score
        df_cons_ranking[cols.cons_tot_wt_scr] += df_cons_ranking[metric_code]

    # Sort the values and rank
    df_cons_ranking = df_cons_ranking.sort_values(by=cols.cons_tot_wt_scr, \
                                    ascending=False)

    df_cons_ranking[cols.rank_col] = df_cons_ranking[cols.cons_tot_wt_scr]\
                                                    .rank(ascending=False, method='min')

    
    return df_cons_ranking
        




