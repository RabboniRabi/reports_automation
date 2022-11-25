"""
Module with utility functions to perform ranking of data
"""


def calc_ranking(df, ranking_type, ranking_args_dict):
    """
    Function to calculate ranking for data based on the type of ranking given.
    The function uses a local dictionary to match the ranking type and 
    calls the appropriate ranking function which will calculate and return the rank.

    Paramters:
    ----------
    ranking_type: str
        The type of ranking to be used to calculate the ranking for the data
    *params:
        The parameters to be passed to the ranking function    
    """
    ranking_func = ranking_funcs_dict.get(ranking_type)
    
    return ranking_func(df, ranking_args_dict)

def percent_ranking(df, ranking_args_dict):

    # group_levels, agg_cols, agg_func, frac_col_name, num_col, den_col, rank_col_name, sort=False, ascending=True, tie_method='min'
    """
    Function to rank data based on percentage (value of one column compared to another column)
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    agg_cols: list
        The columns to aggregate the grouping by
    agg_func: str
        The aggregate function to be applied on the aggregated columns (eg: sum, count, mean)
    frac_col_name: str
        The name of a new column with fractional values computed using two columns in the data
    num_col: str
        The name of the column whose values will go in the numerator of percent based ranking calculation
    den_col: str
        The name of the column whose values will go in the denominator of percent based ranking calculation
    sort: bool
        Default: False. Flag to indicate if values need to be sorting when grouping
    ascending: bool
        Default: True. Flag to if values need to be ranking by ascending order
    tie_method: str
        to rank the group of records that have the same value (i.e. ties)

    Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html                        
    
    Returns:
    --------
        The updated DataFrame object with the fractional values used for ranking and the ranking
    """

    # Get the values from the ranking arguments dictionary
    group_levels = ranking_args_dict['group_levels']
    sort = ranking_args_dict['sort']
    agg_cols = ranking_args_dict['agg_cols']
    agg_func = ranking_args_dict['agg_func']
    frac_col_name = ranking_args_dict['frac_col_name']
    num_col = ranking_args_dict['num_col']
    den_col = ranking_args_dict['den_col']
    rank_col_name = ranking_args_dict['rank_col_name']
    sort = ranking_args_dict['sort']
    ascending = ranking_args_dict['ascending']


    # Group by grouping levels and aggregate by given columns and aggregate function
    df_rank = df.groupby(group_levels, as_index=False, sort=sort)[agg_cols].agg(agg_func)

    # Calculate fraction of values (to be used for ranking)
    df_rank[frac_col_name] = (df_rank[num_col]/df_rank[den_col])
    df_rank[rank_col_name] = df_rank[frac_col_name].rank(ascending=ascending)
    df_rank = df_rank.reset_index()

    return df_rank


# Define a dictionary of ranking functions
ranking_funcs_dict = {
    'percent_ranking': percent_ranking
}