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
        'sort' : True,
        'ascending' : False
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
    #sort = ranking_args_dict['sort']
    ascending = ranking_args_dict['ascending']
    if 'show_rank_col' in ranking_args_dict and ranking_args_dict['ranking_args_dict']:
        show_rank_col = True
    else:
        show_rank_col = False

    # If grouping levels is given
    """if (group_levels is not None and 'agg_dict' in ranking_args_dict):
        agg_dict = ranking_args_dict['agg_dict']
        # Group by grouping levels and aggregate by given columns and aggregate function
        df_rank = df.groupby(group_levels, as_index=False, sort=sort).agg(agg_dict)
    else:
        df_rank = df.copy()"""

    # Group the data for ranking, if ranking level grouping configuration is given in ranking_args
    df_rank = _group_data_for_ranking(df, ranking_args_dict)

    # Calculate fraction of values (to be used for ranking)
    df_rank[cols.ranking_value] = (df_rank[num_col]/df_rank[den_col])
    df_rank[cols.ranking_value].fillna(0, inplace=True)


    df_rank = _sort_and_rank(df_rank, cols.ranking_value, ascending, show_rank_col)
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

def _group_data_for_ranking(df, ranking_args):
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
    # If the grouping before ranking configuration is present
    if 'ranking_group_level' in ranking_args and 'agg_dict' in ranking_args:

        ranking_group_level = ranking_args['ranking_group_level']
        agg_dict = ranking_args['agg_dict']
        sort = ranking_args_dict['sort']

        # If grouping level list and grouping aggregate dictionary is not empty
        if len(ranking_group_level) > 0 and agg_dict:
            # Group the data
            df_rank = df.groupby(ranking_group_level, as_index=False, sort=sort).agg(agg_dict)
    else:
        return df.copy() # Check if copy or original can be sent




def _sort_and_rank(df, ranking_val_col, ascending, show_rank):
    """
    Function to sort and rank the data based on values in a specified column.

    The data can be plain sorted or sorted along with a rank column. The order
    of sorting can also be specified.

    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be sorted and ranked
    ranking_val_col: str
        The name of the column whose columns are to be sorted and ranked
    ascending: bool
        Whether data is to be sorted in ascending order
    show_rank: bool
        Flag indicating if rank column needs to be shown.

    Return:
    -------
    Pandas DataFrame object of sorted and if configured, ranked data    
    """

    # Sort the values
    df.sort_values(by[ranking_val_col], ascending=ascending, inplace=True)
    
    # If rank is to be shown in the data, add the rank column to the data
    if show_rank:
        df[cols.rank_col] = df[cols.ranking_value].rank(method="min")

    # Add the ranking value description to the ranked data
    df[cols.ranking_value_desc] = ranking_val_desc
  
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
