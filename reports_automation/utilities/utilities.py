"""
Module with utility functions that can be commonly used across the project.
"""

from datetime import datetime

import pandas as pd



def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = ''):
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

