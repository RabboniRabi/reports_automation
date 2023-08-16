"""
Module with utility functions that can be commonly used across the project.
"""

from datetime import datetime

import pandas as pd

def get_today_date():
    """
    Function to return a string representation of the current day's date

    Returns:
    -------
    The current date as a 'DD:MM:YY' format string
    """
    return datetime.now().strftime('%d-%m-%y')


def xlookup(lookup_value, lookup_array, return_array, if_not_found = ''):
    """
    Function to perform the XLOOKUP function in Excel
    """
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return 0 if if_not_found == '' else if_not_found

    else:
        return match_value.tolist()[0]

def filter_dataframe_column(df, column_name, values_in):
    """
    Function to filter a data frame for given values in a given column
    Parameters:
    ----------
    df: Pandas DataFrame object
        The data set to filter
    column_name: str
        The name of the column to filter in
    values: list
        The list of values to filter for
    Returns:
    -------
    The filtered Pandas DataFrame object            
    """
    df_filtered = df[df[column_name].isin(values_in)]
    return df_filtered

def filter_dataframe_not_in_column(df, column_name, values_in):
    """
    Function to filter a data frame for columns values other than those given
    Parameters:
    ----------
    df: Pandas DataFrame object
        The data set to filter
    column_name: str
        The name of the column to filter in
    values: list
        The list of values to filter out
    Returns:
    -------
    The filtered Pandas DataFrame object   
    """
    df_filtered = df[~df[column_name].isin(values_in)]
    return df_filtered

def filter_column_le(df, column_name, threshold_value):
    """
    Function to filter a dataframe object by values less than or equal to given threshold value
    Parameters:
    ----------
    df: Pandas DataFrame object
        The data set to filter
    column_name: str
        The name of the column to filter in
    threshold_value: 
        The threshold value
    Returns:
    -------
    The filtered Pandas DataFrame object   
    """
    df_filtered = df[df[column_name].le(threshold_value)]       
    return df_filtered


def filter_column_ge(df, column_name, threshold_value):
    """
    Function to filter a dataframe object by values greater than or equal to given threshold value
    Parameters:
    ----------
    df: Pandas DataFrame object
        The data set to filter
    column_name: str
        The name of the column to filter in
    threshold_value: 
        The threshold value
    Returns:
    -------
    The filtered Pandas DataFrame object   
    """
    df_filtered = df[df[column_name].ge(threshold_value)]       
    return df_filtered

def columns_subset(df, columns):
    """
    Function to return a given dataframe object with only a subset of given columns
    Parameters:
    ----------
    df: Pandas DataFrame object
        The data set to filter
    columns: list
        The list of columns (by name) to be in the data subset
    Returns:
    -------
    A Pandas DataFrame object with a subset of columns    
    """
    df_subset = pd.DataFrame()
    for column in columns:
        df_subset[column] = df[column]
    return df_subset

def pivot_table_w_subtotals(df, values, indices, columns, aggfunc, fill_value):
    """
    Adds tabulated subtotals to pandas pivot tables with multiple hierarchical indices.
    
    Parameters:
    ----------
    df: Pandas DataFrame object
        dataframe used in pivot table
    values: list
        Columns to aggregrate
    indices: list
        The indices to pivot on - ordered list of indices to aggregrate by
    columns: list
        The columns whose values will each become a column in the resulting pivot
    aggfunc: str
        The name of function to be used to aggregrate (np.max, np.mean, np.sum, etc)
    fill_value:
        Value to be used in place of empty cells
    
    Returns:
    -------
    Flat table with data aggregrated and tabulated
    """
    listOfTable = []
    subtotal_name_cols = 0 # The column index where cell values are appended with the string: total (To indicate subtotals)
    for indexNumber in range(len(indices)):
        n = indexNumber + 1
        # Pivot on subset of indices 0 to n
        table = pd.pivot_table(df,values=values,index=indices[:n],columns=columns,aggfunc=aggfunc,fill_value=fill_value).reset_index()
        if subtotal_name_cols < len(indices) - 1: # No need to add the string total to the last of the index columns
            table[indices[subtotal_name_cols]] = table[indices[subtotal_name_cols]] + ' Total ' # Add the string total to the name
            subtotal_name_cols += 1 # Increment by 1
        for column in indices[n:]:
            #print(table)
            table[column] = '' # make the columns of indices n to length(indices) blank
        listOfTable.append(table)
    concatTable = pd.concat(listOfTable).sort_index()
    concatTable = concatTable.set_index(keys=indices)
    return concatTable.sort_index(axis=0,ascending=True)


def get_date_appended_excel_filename(file_name):
    """
    utilities function to get today's date as a string
    Parameters:
    -----------
    file_name: str
        The name of the file to append the date to
    Returns:
    --------
    String value of today's date in dd-mm-yy format
    """
    now = datetime.now()
    return file_name + '_' + now.strftime('%d-%m-%y') + '.xlsx'



def insert_row(df, row_number, row_value):
    """
    Function to insert a given value at a specified row in the dataframe
    by slicing, adding and concatinating the dataframe

    Implementation taken from: 
    https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/

    Parameters:
    ----------
    df: Pandas DataFrame object
        The data frame into which a row has to be inserted
    row_number: int
        The row index to insert the value at
    row_value:
        The value to be inserted into the data frame object        
    """   
    # Slice the data frame into two along the row_number value
    df_upper = df[0:row_number]
    df_lower = df[row_number:]

    # Insert the value to the bottom of the upper slice
    df_upper.loc[row_number] = row_value

    # Concatenate the two sliced data frames
    df_result = pd.concat([df_upper,df_lower])

    # Reassign the index labels
    df_result.index = [*range(df_result.shape[0])]
  
    # Return the updated dataframe
    return df_result




def build_row(master_columns, df_partial_row, text_append_dict):
    """
    Function to build a row containing all the columns in the master dataframe.

    Where there is a matching column in the partial dataframe row, 
    the value in the cell is placed in the new row.
    Where no corresponding column is present in the subset data frame, 
    empty value is placed in the corresponding cell.

    Parameters:
    ----------
    master_columns numpy array
        Collection of column names of the master dataframe 
    df_partial_row Pandas DataFrame object
        A dataframe object with a single row and partial columns of the master dataframe
    text_append_dict Dictionary
        A dictionary of column names key and text values. The dictionary will be used
        to append text to cell values at column names    

    Returns:
    -------
    A row of values compatible with the columns in the master dataframe. This row can 
    now be directly inserted into the dataframe
    """

    subset_columns = df_partial_row.columns.values
    new_row = []

    # For each column in the list of master columns
    for column in master_columns:
        # If column is also in the column of the partial dataframe
        if column in subset_columns[:]:

            row_index = df_partial_row.index.tolist()[0] # Get the index of the single row
            
            # Get any additional text to append to the value at this column
            if column in text_append_dict.keys():
                append_text = ' ' + text_append_dict[column]
                cell_value = str(df_partial_row.loc[row_index, column]) + append_text
            else:
                cell_value = df_partial_row.loc[row_index, column]   

            # Append value to the position in this column
            new_row.append(cell_value)
        else:
            # Append empty value
            new_row.append('')   
    return new_row    


def filter_group_count_valid_values(df, group_levels, filter_columns_regex_dict):
    """
    Function to filter data by taking only those values that match a given regex pattern,
    apply grouping on given grouping columns and count the number of valid values on
    the columns the regex pattern was matched on.

    Parameters:
    ----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    filter_columns_regex_dict: dict
        A column - regex, key - value pair dictionary
        This dictionary will be used to filter values in the column by matching only the values
        given in the regex
        eg: {
            'col_a' : '[1-9].',
            'col_b' : '(a|h|e)+
        }
    Returns:
    -------
    DataFrame object of filtered and grouped data    
    """
    first_iteration = True
    for column in filter_columns_regex_dict.keys():
        # Filter the data by accepted values for a column
        accepted_values_regex = filter_columns_regex_dict[column]
        df_col_accepted_vals = filter_df_by_regex_match(df, column, accepted_values_regex)
        # Apply grouping on the filtered data and count the accepted values in the columns
        df_grouped = df_col_accepted_vals.groupby(group_levels,sort=False)[column].count().reset_index()

        # If iterating for the first time, there wont be previous grouping to merge
        if first_iteration:
            df_filtered_grouped = df_grouped
            first_iteration = False
        else:
            # columns to merge will be grouping columns plus the current iterated column
            merge_cols = group_levels + [column]    
            df_filtered_grouped = df_filtered_grouped.merge(df_grouped[merge_cols], on=group_levels, how='outer').reset_index()

    return df_filtered_grouped      


def filter_df_by_regex_match(df, column, accepted_values_regex):
    """
    Function to filter data by matching values in a column with corresponding regex pattern.
    
    Parameters:
    ----------
    df: Pandas DataFrame
        The raw data
    column: str
        The column on which to filter the data
    accepted_values_regex: str
        A regex pattern to be used to match values in a column        
    Returns:
    -------
    DataFrame object of data filtered on a column    
    """
    # Filter the data by accepted values for a column
    df_col_accepted_vals = df[df[column].str.match(accepted_values_regex)]

    return df_col_accepted_vals


def get_grouping_level_wise_col_values_count(df, group_levels, column, col_values):
    """
    Function to get the count of number of occurences of each distinct value in a given column
    at given grouping levels.

    Parameters:
    -----------
    df: Pandas DataFrame
        The raw data
    group_levels: list
        The list of columns to group by
    column: str
        The column in which to count the number of occurences of each distinct value
    col_values: list
        A subset of column values to get the count for
    Returns:
    --------
    DataFrame object with count of support provided in different categories
    """

    # Pivot the table - group to grouping levels and count the number of distinct values in column
    df_pivot = pd.pivot_table(df, index=group_levels, columns=column,
                aggfunc='size', fill_value=0, sort=False).reset_index()

    # Filter the result of the pivot with columns containing grouping levels and supported categories
    selected_columns = group_levels + col_values            

    df_supp_cat_count = df_pivot[selected_columns]

    return df_supp_cat_count


def is_any_row_common(df_larger, df_smaller):
    """
    Function to check if atleast one row in both of the given dataframes is common.
    Returns True if so. False otherwise.

    Parameters:
    -----------
    df_larger: The larger of the two dataframes to be compared. Nominal.
    df_smaller: The smaller of the two dataframes to be compared. Nominal.

    Returns:
    -------
    True if atleast one row is common in both of the given dataframes. False otherwise.
    """

    # Get the cell wise matches of the smaller data frame with the larger dataframe
    df_cell_wise_matches = df_smaller.isin(df_larger)
    # Get the row wise True matches (True if all cells in a row are True. False otherwise)
    df_rows_wise_matches = df_cell_wise_matches.all(axis='columns')
    # Check if any row match done above was true
    any_row_matches = df_rows_wise_matches.any(axis=None)

    return any_row_matches

def rank_cols_insert(df, ranking_args_dict, rank_frac=False):
    """
    Function to rank the data based on the specific columns.

    Parameters:
    -----------
    df: Pandas Data Frame
        Data to rank
    ranking_args_dict: dict
        For Example:
        "cols.curr_eng_marks":{
            "insert_rank_col": "cols.eng_rank_state",
            "index": 1,
            "ascending": "False"
        }

    rank_frac: bool
        True - If the rank be represented by rank/total number of records.
        For Example: (15/175, 16/175...)
        Default is False - Rank be represented as (1, 2 ,3...)

    Returns:
    ------
    Ranked Dataframe
    """
    for sort_col, rank_args in ranking_args_dict.items():
        # Sort the dataframe based on the sort column
        df.sort_values(by=sort_col, ascending=rank_args["ascending"], inplace=True)
        # Calculate the index where the rank column needs to be inserted
        index_col = df.columns.get_loc(sort_col) + rank_args["index"]
        # Inserting the rank column
        df.insert(index_col, rank_args["insert_rank_col"], range(1, 1+len(df)))

        if rank_frac is True:
            total = len(df)
            df[rank_args["insert_rank_col"]] = df[rank_args["insert_rank_col"]].apply(lambda rank: str(rank_args["insert_rank_col"]) + '/' + str(total))

    return df




