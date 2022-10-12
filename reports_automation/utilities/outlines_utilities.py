import pandas as pd

"""
Module with utility functions to perform excel outlines operations on datasets
"""


def  build_level_outline_ranges_dict(df, df_subtotal_rows, level_subtotal_cols_dict, group_cols_agg_func_dict):
    """
    Function to build the level to ranges mapping for applying the excel outlines functionality.
    Parameters:
    -----------
    df: Pandas dataframe object
        The master data
    df_subtotal_rows: Pandas dataframe object
        The ggregated subtotal rows to skip from outlines
    level_subtotal_cols_dict: dictionary
        Dictionary of outline level - subtotal columns key value pairs 
    group_cols_agg_func_dict: dict
        A grouping column - aggregate function dictionary. This dictionary contains the columns
        to group by as keys and their corresponding aggregating function as values. Aggregation
        is not applied in this function. It is merely used to convert groupby Objects to DataFrame.
        Not an elegant way to do things. Yes.        
    Returns:
    --------
    A dictionary of level to ranges key-value pairs
    """
    level_outline_ranges_dict = dict()
    # Get a DataFrame without the subtotal rows
    df_without_subtotals = pd.concat([df, df_subtotal_rows, df_subtotal_rows]).drop_duplicates(keep=False)

    for outline_level in level_subtotal_cols_dict.keys():
        
        subtotal_col = level_subtotal_cols_dict[outline_level]

        # Get an aggregate column and function to be used to convert
        # groupby object to DataFrame object
        agg_col = list(group_cols_agg_func_dict.keys())[0]
        agg_func = group_cols_agg_func_dict[agg_col]
        # Get unique subtotal column values
        df_without_subtotals_grouped = df_without_subtotals.groupby(
            [subtotal_col], as_index=False,sort=False)[agg_col].agg(agg_func)

        # For each row in df_without_subtotals_grouped
        for i in range(0, df_without_subtotals_grouped.shape[0]):
            # Get the value of the cell in ith row and in column: subtotal_col
            subtotal_col_val = df_without_subtotals_grouped.loc[i, subtotal_col]
            if (subtotal_col_val != ''):

                # Get the indices in the master data frame matching this value in the same column
                matching_indices = df.index[df[subtotal_col] == subtotal_col_val].tolist()
                # Sort the list of matching indices (Will already be sorted. Just in case)
                matching_indices.sort()

                # Collect the ranges to apply the excel outline for
                outline_range = tuple((matching_indices[0], matching_indices[len(matching_indices) - 1]))

                # Add the range to the level_outline_ranges_dict dictionary
                if outline_level not in level_outline_ranges_dict.keys():
                    level_outline_ranges_dict[outline_level] = [outline_range]
                else:
                    level_outline_ranges_dict[outline_level].append(outline_range) 
    
    return level_outline_ranges_dict




def apply_outlines(ws, level_ranges_dict):
    """
    Function to apply Excel outlines to a given openpyxl workbook object
    Parameters:
    ----------
    ws: An openpyxl worksheet object
    level_ranges_dict: A dictionary of level ranges key values
        where ranges is a list of tuples for each level
        and each tuple contains the start index and end index of the range
        Eg: {
            '1': [
                (2,10),(11,20),(21,30)
                ],
            '2': [
                (2,4),(2,9),(11,16),(17,20),(21,24),(25,30)
                ]    
            }
    """

    ws.sheet_properties.outlinePr.summaryBelow = False


    # For each outline level
    for level in sorted(level_ranges_dict.keys()):
        # For each range tuple at each outline level
        for outline_range in level_ranges_dict[level]:
            # Apply the outline
            ws.row_dimensions.group(outline_range[0]+3, outline_range[1]+3, outline_level=level,hidden=False)

    return ws            
