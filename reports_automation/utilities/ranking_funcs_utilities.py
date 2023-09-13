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
    ranking_val_desc = ranking_args_dict['ranking_val_desc']
    num_col = ranking_args_dict['num_col']
    den_col = ranking_args_dict['den_col']

    
    # Group the data for ranking, if ranking level grouping configuration is given in ranking_args
    #df_rank = _group_data_for_ranking(df, ranking_args_dict)

    # Calculate fraction of values (to be used for ranking)
    df_rank[cols.ranking_value] = (df[num_col]/df[den_col])
    df_rank[cols.ranking_value].fillna(0, inplace=True)


    df_rank = _sort_rank_and_show_hide_cols(df_rank, ranking_args_dict)


    """df_rank[cols.rank_col] = df_rank[cols.ranking_value].rank(ascending=ascending, method='min')
    
    # Add the ranking value description to the ranked data
    df_rank[cols.ranking_value_desc] = ranking_val_desc
    
    
    # Sort by ranking if specified
    if sort:
        df_rank.sort_values(by=[cols.rank_col], inplace=True)

    df_rank = df_rank.reset_index()    """

    return df_rank


def percent_ranking_agg(df, group_levels, ranking_args_dict):
    """
    Function similar to percent_ranking to rank data based on percentage.
    (value of numerator is aggregate sum of given list of numerator columns. Similar for denominator)
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    group_levels: list
        The list of columns to group by
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
    ranking_val_desc = ranking_args_dict['ranking_val_desc']
    num_cols = ranking_args_dict['num_col']
    den_cols = ranking_args_dict['den_col']
    sort = ranking_args_dict['sort']
    ascending = ranking_args_dict['ascending']

    # If grouping levels is given
    if (group_levels is not None):
        # Group by grouping levels and aggregate by given columns and aggregate function
        df_rank = df.groupby(group_levels, as_index=False, sort=sort).agg(agg_dict)
    else:
        df_rank = df.copy()

    # Sum values in the numerator and denominator columns
    num_agg = 0
    for col in num_cols:
        num_agg += df_rank[col]
    
    den_agg = 0
    for col in den_cols:
        den_agg += df_rank[col]
    

    # Calculate fraction of values (to be used for ranking)
    df_rank[cols.ranking_value] = (num_agg/den_agg)
    df_rank[cols.ranking_value].fillna(0, inplace=True)
    df_rank[cols.rank_col] = df_rank[cols.ranking_value].rank(ascending=ascending, method='min')
    
    # Add the ranking value description to the ranked data
    df_rank[cols.ranking_value_desc] = ranking_val_desc
    
    
    # Sort by ranking if specified
    if sort:
        df_rank.sort_values(by=[cols.rank_col], inplace=True)

    df_rank = df_rank.reset_index()    

    return df_rank


def avg_ranking(df, group_levels, ranking_args_dict):
    """
    Function to rank data based on result of averaging a list of values
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    group_levels: list
        The list of columns to group by
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
    ranking_val_desc = ranking_args_dict['ranking_val_desc']
    avg_cols = ranking_args_dict['avg_cols']
    sort = ranking_args_dict['sort']
    ascending = ranking_args_dict['ascending']

    # If grouping levels is given
    if (group_levels is not None):
        # Group by grouping levels and aggregate by given columns and aggregate function
        df_rank = df.groupby(group_levels, as_index=False, sort=sort).agg(agg_dict).reset_index()
    else:
        df_rank = df.copy()


    # Calculate average of given columns
    for i in range(0, len(avg_cols)):
        if i == 0:
            total_series = pd.Series(df_rank[avg_cols[i]])
        else:
            total_series = total_series + df_rank[avg_cols[i]]

    no_of_items = len(avg_cols)
    df_rank[cols.ranking_value] = (total_series/no_of_items)
    df_rank[cols.ranking_value].fillna(0, inplace=True)

    # Sort and rank the values
    df_rank[cols.rank_col] = df_rank[cols.ranking_value].rank(ascending=ascending, method='min')
    
    # Add the ranking value description to the ranked data
    df_rank[cols.ranking_value_desc] = ranking_val_desc
    
    
    # Sort by ranking if specified
    if sort:
        df_rank.sort_values(by=[cols.rank_col], inplace=True)

    df_rank = df_rank.reset_index()    

    return df_rank

def number_ranking(df, group_levels, ranking_args_dict):
    """
    Function to rank data based on value given in a specified column.

    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
    group_levels: list
        The list of columns to group by
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
    # Get the values from the ranking arguments dictionary
    agg_dict = ranking_args_dict['agg_dict']
    ranking_val_desc = ranking_args_dict['ranking_val_desc']
    sort = ranking_args_dict['sort']
    ascending = ranking_args_dict['ascending']
    # Get the name of the column to rank on
    ranking_col = ranking_args_dict['ranking_col']

    # If grouping levels is given
    if (group_levels is not None):
        df_rank = df.groupby(group_levels, as_index=False, sort=sort).agg(agg_dict)
    else:
        df_rank = df.copy()

    # Rename source data column to be ranked as ranking value - needed by rest of ranking code
    df_rank.rename(columns={ranking_col: cols.ranking_value}, inplace=True)

    # Sort and rank the values
    df_rank[cols.rank_col] = df_rank[cols.ranking_value].rank(ascending=ascending, method="min")

    # Add the ranking value description to the ranked data
    df_rank[cols.ranking_value_desc] = ranking_val_desc

    # Sort by ranking if specified
    if sort:
        df_rank.sort_values(by=[cols.rank_col], inplace=True)
    df_rank = df_rank.reset_index()

    return df_rank




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

    # Sort the values
    df.sort_values(by[cols.ranking_value], ascending=ranking_args_dict['ascending'], inplace=True)

    # Add a rank column if flag indicates that rank should be shown
    if 'show_rank_col' in ranking_args_dict and ranking_args_dict['show_rank_col']:
        df[ranking_args['rank_col_name']] = df[cols.ranking_value].rank(method="min")
    
    # Check if flag indicates that rank value should be shown
    if 'show_rank_val' in ranking_args_dict and ranking_args_dict['show_rank_val']:
        # Rename the ranking value description
        df.rename(columns={cols.ranking_value:ranking_args_dict['ranking_val_desc']}, inplace=True)
    else if 'show_rank_val' in ranking_args_dict and not ranking_args_dict['show_rank_val']:
        # Drop the rank value column
        df_rank.drop(columns=[cols.ranking_value], inplace=True)
  
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
