"""
Module with utility functions to perform different types of ranking 
- Currently there is only percent type ranking
"""
import sys
sys.path.append('../')
import utilities.column_names_utilities as cols

import pandas as pd

def percent_ranking(df, ranking_args_dict):
    """
    Function to rank data based on percentage (value of one column compared to another column)
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : true,
        'ascending' : false,
        'show_rank_col' : true/false,
        'rank_col_name' : 'to be given if show_rank_col is true',
        'show_rank_val: : true/false,
        'ranking_val_desc' : 'to be given if show_rank_val is true'
        }

    Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html                        
    
    Returns:
    --------
        The updated DataFrame object with the fractional values used for ranking and the ranking
    """

    # Get the values from the ranking arguments dictionary
    num_col = ranking_args_dict['num_col']
    den_col = ranking_args_dict['den_col']

    # Calculate fraction of values (to be used for ranking)
    df[cols.ranking_value] = (df[num_col]/df[den_col])
    df[cols.ranking_value].fillna(0, inplace=True)

    # Sort the data, rank it and show/hide columns based on the configuration
    df = _sort_rank_and_show_hide_cols(df, ranking_args_dict)

    return df


def percent_ranking_agg(df, ranking_args_dict):
    """
    Function similar to percent_ranking to rank data based on percentage.
    (value of numerator is aggregate sum of given list of numerator columns. Similar for denominator)
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
        'ranking_val_desc' : '% moved to CP',
        'num_col' : ['class_1', 'class_2', 'class_3'],
        'den_col' : ['Total'],
        'sort' : True,
        'ascending' : False
        }

    Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html                        
    
    Returns:
    --------
        The updated DataFrame object with the fractional values used for ranking and the ranking
    """

    # Get the values from the ranking arguments dictionary
    agg_dict = ranking_args_dict['agg_dict']
    num_cols = ranking_args_dict['num_col']
    den_cols = ranking_args_dict['den_col']    

    # Sum values in the numerator and denominator columns
    num_agg = 0
    for col in num_cols:
        num_agg += df[col]
    
    den_agg = 0
    for col in den_cols:
        den_agg += df[col]
    
    # Calculate fraction of values (to be used for ranking)
    df[cols.ranking_value] = (num_agg/den_agg)
    df[cols.ranking_value].fillna(0, inplace=True)
    # Sort the data, rank it and show/hide columns based on the configuration
    df = _sort_rank_and_show_hide_cols(df, ranking_args_dict)

    return df


def avg_ranking(df, ranking_args_dict):
    """
    Function to rank data based on result of averaging a list of values
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
        'ranking_val_desc' : '% moved to CP',
        'avg_cols' : ['class_1', 'class_2', 'class_3', 'class_4']
        'sort' : True,
        'ascending' : False
        }

    Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html                        
    
    Returns:
    --------
        The updated DataFrame object with the average values used for ranking and the ranking
    """
    # Get the values from the ranking arguments dictionary
    agg_dict = ranking_args_dict['agg_dict']
    avg_cols = ranking_args_dict['avg_cols']

    # Calculate average of given columns
    for i in range(0, len(avg_cols)):
        if i == 0:
            total_series = pd.Series(df[avg_cols[i]])
        else:
            total_series = total_series + df[avg_cols[i]]

    no_of_items = len(avg_cols)
    df[cols.ranking_value] = (total_series/no_of_items)
    df[cols.ranking_value].fillna(0, inplace=True)
    # Sort the data, rank it and show/hide columns based on the configuration
    df = _sort_rank_and_show_hide_cols(df, ranking_args_dict)

    return df

def number_ranking(df, ranking_args_dict):
    """
    Function to rank data based on value given in a specified column.

    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
        'ranking_val_desc' : 'Student teacher ratio',
        'ranking_col' : 'student_teacher_ratio'
        'sort' : True,
        'ascending' : True
        }

    Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html

    Returns:
    --------
        The updated DataFrame object with the ranking.
    """

    # Sort the data, rank it and show/hide columns based on the configuration
    #df[cols.ranking_value] = df[ranking_args_dict['ranking_col']]
    df.rename(columns={
        ranking_args_dict['ranking_col']: cols.ranking_value
    },inplace=True)
    df = _sort_rank_and_show_hide_cols(df, ranking_args_dict)

    return df




def _sort_rank_and_show_hide_cols(df, ranking_args_dict):
    """
    Function to sort and rank the data based on values in a specified column.

    The data can be plain sorted or sorted along with a rank column. The order
    of sorting can also be specified.

    The rank values can also be dropped if the show_rank_val in the config is false.

    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be sorted and ranked
    ranking_args_dict: dict
        A dictionary of parameter name - parameter value key-value pairs to be used for calculating the rank
        Eg: ranking_args_dict = {
        'group_levels' : ['district', 'name', 'designation'],
        'agg_dict': {'schools' : 'count', 'students screened' : 'sum'},
        'ranking_val_desc' : '% moved to CP',
        'num_col' : 'class_1',
        'den_col' : 'Total',
        'sort' : true,
        'ascending' : false,
        'show_rank_col' : true/false,
        'rank_col_name' : 'to be given if show_rank_col is true',
        'show_rank_val: : true/false,
        'ranking_val_desc' : 'to be given if show_rank_val is true'
        }

    Return:
    -------
    Pandas DataFrame object of sorted and if configured, ranked data    
    """
    """

    if ranking_args_dict['ranking_type'] == 'number_ranking':
        
        If ranking type is number ranking, rename the ranking column to generic 'Ranking Value'
        for the execution of this function. No need to rename it back as ranking_col and ranking_val_desc
        can be given as same in the config. 
        'Ranking Value' gets renamed to ranking_val_desc during the execution of this function
        
        df.rename(columns={ranking_args_dict['ranking_col']: cols.ranking_value}, inplace=True)
    """

    # Get the ascending flag
    ascending = ranking_args_dict['ascending']   

    # Sort the values if flag is true
    if ranking_args_dict['sort']: 
        df.sort_values(by=[cols.ranking_value], ascending=ascending, inplace=True)

    # Add a rank column if flag indicates that rank should be shown
    if 'show_rank_col' in ranking_args_dict and ranking_args_dict['show_rank_col']:
        # Check if data needs to be ranked within a group
        if 'rank_within_parent_group' in ranking_args_dict and ranking_args_dict['rank_within_parent_group']:
            parent_grouping_levels = ranking_args_dict['rank_within_parent_grouping_levels']
            df[ranking_args_dict['rank_col_name']] = df.groupby(parent_grouping_levels)[cols.ranking_value]\
                                        .rank(ascending=ascending, method="min")
        else:
            # Else, rank the data
            df[ranking_args_dict['rank_col_name']] = df[cols.ranking_value].rank(ascending=ascending, method="min")
    
    # Check if flag indicates that rank value should be shown
    if 'show_rank_val' in ranking_args_dict and ranking_args_dict['show_rank_val']:
        # Rename the ranking value description
        df.rename(columns={cols.ranking_value:ranking_args_dict['ranking_val_desc']}, inplace=True)
    elif 'show_rank_val' in ranking_args_dict and not ranking_args_dict['show_rank_val']:
        # Drop the rank value column
        df.drop(columns=[cols.ranking_value], inplace=True)
  
    df = df.reset_index()

    return df



def get_ranking_funcs():
    """
    Function to return names of available ranking functions

    Returns:
    -------
    Dictionary of name - function name key-value pairs
    """
    return ranking_funcs_dict
   
# Define a dictionary of ranking functions
ranking_funcs_dict = {
    'percent_ranking' : percent_ranking,
    'multiple_columns_percent_ranking' : percent_ranking_agg,
    'average_ranking': avg_ranking,
    'number_ranking' : number_ranking
}    
