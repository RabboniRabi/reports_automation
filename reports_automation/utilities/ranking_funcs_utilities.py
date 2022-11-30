"""
Module with utility functions to perform different types of ranking 
- Currently there is only percent type ranking
"""


# Define the name of the columns with the ranks
rank_col = 'Rank'
# Define the name of the column in ranked data with values that will be used to calculate ranking
ranking_value_col = 'Ranking Value'
# Define the name of the column with short description of the values used for ranking
ranking_value_desc_col = 'Ranking Value Description'



def percent_ranking(df, ranking_args_dict):

    # group_levels, agg_cols, agg_func, frac_col_name, num_col, den_col, rank_col_name, sort=False, ascending=True, tie_method='min'
    """
    Function to rank data based on percentage (value of one column compared to another column)
    
    Parameters:
    -----------
    df: Pandas DataFrame
        The data to be ranked
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
    ranking_val_desc = ranking_args_dict['ranking_val_desc']
    num_col = ranking_args_dict['num_col']
    den_col = ranking_args_dict['den_col']
    sort = ranking_args_dict['sort']
    ascending = ranking_args_dict['ascending']


    # Group by grouping levels and aggregate by given columns and aggregate function
    df_rank = df.groupby(group_levels, as_index=False, sort=sort)[agg_cols].agg(agg_func)

    # Calculate fraction of values (to be used for ranking)
    df_rank[ranking_value_col] = (df_rank[num_col]/df_rank[den_col])
    df_rank[rank_col] = df_rank[ranking_value_col].rank(ascending=ascending)
    
    # Add the ranking value description to the ranked data
    df_rank[ranking_value_desc_col] = ranking_val_desc
    
    
    # Sort by ranking if specified
    if sort:
        df_rank.sort_values(by=[rank_col], inplace=True)

    df_rank = df_rank.reset_index()    

    return df_rank


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
    'percent_ranking': percent_ranking
}    
