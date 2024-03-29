"""
Module with utility functions that can be commonly used across the project.
"""

from datetime import datetime
from datetime import date
import datetime as dt

import pandas as pd


def get_today_date():
    """
    Function to return a string representation of the current day's date

    Returns:
    -------
    The current date as a 'DD:MM:YY' format string
    """
    return datetime.now().strftime('%d-%m-%y')


def get_curr_year():
    """
    Function to return the current year

    Returns:
    -------
    The current year in 'YYYY' format int
    """
    return date.today().year


def get_prev_year():
    """
    Function to return the previous year

    Returns:
    -------
    The previous year in 'YYYY' format int
    """
    return date.today().year - 1

def get_curr_month():
    """
    Function to return a string representation of the current month name

    Returns:
    --------
    The current month in a 3 letter abbreviated format
    """
    return datetime.now().strftime('%h')

def get_prev_month():
    """
    Function to return a string representation of the previous month name

    Returns:
    --------
    The previous month in a 3 letter abbreviated format
    """
    today = dt.date.today()
    first = today.replace(day=1)

    last_month = first - dt.timedelta(days=1)

    return last_month.strftime("%h")

def get_year_of_prev_month():
    """
    Function to return a string representation of the year of 
    the month previous to the current month

    Returns:
    --------
    The current year in YYYY format
    """
    today = dt.date.today()
    first = today.replace(day=1)

    last_month = first - dt.timedelta(days=1)

    return last_month.strftime("%Y")

def get_curr_year_as_str():
    """
    Function to return a string representation of the current year

    Returns:
    --------
    The current year in YYYY format
    """
    return datetime.now().strftime('%Y')


def xlookup(lookup_value, lookup_array, return_array, if_not_found=''):
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

def filter_dataframe(df, filter_dict, include=True):
    """
    Function to filter the dataframe for multiple columns either by including or 
    excluding the given set of values.

    Parameters:
    ----------
    df: Pandas Dataframe
        The data to filter
    filter_dict: dict
        {'Column_names' : [values need to be filtered]}
    include: bool
        Default is true
        If include is false, the values corresponding to the column will be excluded
        else it will be included

    Returns:
    --------
    Filtered dataframe
    """
    for col_name, values in filter_dict.items():
        if include:
            df = filter_dataframe_column(df, col_name, values)
        else:
            df = filter_dataframe_not_in_column(df, col_name, values)
    return df

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
    subtotal_name_cols = 0  # The column index where cell values are appended with the string: total (To indicate subtotals)
    for indexNumber in range(len(indices)):
        n = indexNumber + 1
        # Pivot on subset of indices 0 to n
        table = pd.pivot_table(df, values=values, index=indices[:n], columns=columns, aggfunc=aggfunc,
                               fill_value=fill_value).reset_index()
        if subtotal_name_cols < len(indices) - 1:  # No need to add the string total to the last of the index columns
            table[indices[subtotal_name_cols]] = table[indices[
                subtotal_name_cols]] + ' Total '  # Add the string total to the name
            subtotal_name_cols += 1  # Increment by 1
        for column in indices[n:]:
            # print(table)
            table[column] = ''  # make the columns of indices n to length(indices) blank
        listOfTable.append(table)
    concatTable = pd.concat(listOfTable).sort_index()
    concatTable = concatTable.set_index(keys=indices)
    return concatTable.sort_index(axis=0, ascending=True)


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
    df_result = pd.concat([df_upper, df_lower])

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

            row_index = df_partial_row.index.tolist()[0]  # Get the index of the single row

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
        df_grouped = df_col_accepted_vals.groupby(group_levels, sort=False)[column].count().reset_index()

        # If iterating for the first time, there wont be previous grouping to merge
        if first_iteration:
            df_filtered_grouped = df_grouped
            first_iteration = False
        else:
            # columns to merge will be grouping columns plus the current iterated column
            merge_cols = group_levels + [column]
            df_filtered_grouped = df_filtered_grouped.merge(df_grouped[merge_cols], on=group_levels,
                                                            how='outer').reset_index()

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


def group_agg_rename(df, grouping_levels, agg_dict: dict, append_str=''):
    """
	Function to group data to given grouping levels, aggregating each data column 
	with its corresponding aggregation function given in the dictionary and
	renaming the columns to relect the aggregated nature of the data.

	Parameters:
	-----------
	df: Pandas DataFrame
		The data to group
	grouping_levels: list
		The list of columns to group the data upto (levels to group)
	agg_dict: dict
        The columns to aggregate and their corresponding functions
	append_st: str
		The string to append to the column name of each of the aggregate column

	Returns:
	-------
	The grouped data
	"""

    # Group and aggregate the data
    df_grouped = df.groupby(grouping_levels, as_index=False).agg(agg_dict)

    # Rename the columns to reflect the aggregated nature of the data
    cols_to_rename = {}
    for agg_col in agg_dict.keys():
        if append_str != '':
            cols_to_rename[agg_col] = agg_col + '_' + agg_dict[agg_col] + '_' + append_str
        else:
            cols_to_rename[agg_col] = agg_col + '_' + agg_dict[agg_col]

    df_grouped.rename(columns=cols_to_rename, inplace=True)

    return df_grouped


def is_any_row_common(df_larger, df_smaller):
    """
    Function to check if atleast one row in both of the given dataframes is common.
    Returns True if so. False otherwise.

    Parameters:
    -----------
    df_larger: Pandas DataFrame
        The larger of the two dataframes to be compared. Nominal.
    df_smaller: Pandas DataFrame
        The smaller of the two dataframes to be compared. Nominal.

    Returns:
    -------
    True if atleast one row is common in both of the given dataframes. False otherwise.
    """

    # Get the cell wise matches of the smaller data frame with the larger dataframe
    df_cell_wise_matches = df_smaller.isin(df_larger)

    return df_cell_wise_matches.any()


def update_master_data(df_master_data, df_new_data):
    """
    Function to update a master(larger) data with new data.

    Both DataFrames are expected to have the same columns.

    New data is concatenated to the master data and duplicates
    are removed.

    Parameters:
    -----------
    df_master_data: Pandas DataFrame
        The master data DataFrame to be updated.
    df_new_data: Pandas DataFrame
        The new data DataFrame to be added to the master data.

    Returns:
    --------
    The updated master data
    """

    # Concatenate the master data with new data
    df_master_data = pd.concat([df_master_data, df_new_data])

    print('data post concat', df_master_data.head())
    # Remove the duplicates
    df_master_data.drop_duplicates(subset=['emis_no'], inplace=True)

    print('data post dropping duplicates', df_master_data.head())

    return df_master_data


def subtract_dfs(df_first, df_second, cols:list, index_col_name: str):
    """
    Function to element wise subtract values in columns
    between two data frame objects.

    Parameters:
    ----------
    df_first: Pandas DataFrame
        The data on the left of the - sign
    df_second: Pandas DataFrame
        The data on the right of the - sign
    cols: list
        The list of columns to subtract
    index_col_name: str
        The name of a column to sort the data by and then subtract them.
        To ensure correct row wise subtraction.
    """

    # Sort the values before subtracting
    df_first = df_first.sort_values(by=index_col_name).set_index(index_col_name)
    df_second = df_second.sort_values(by=index_col_name).set_index(index_col_name)

    df_subtracted = df_first.copy()

    for col in cols:
        if col in df_second and col in df_first:
            df_subtracted[col] = df_first[col] - df_second[col]
        else:
            df_subtracted[col] = 0

    return df_subtracted.reset_index()

def add_dfs(df_first, df_second, cols:list, index_col_name: str):
    """
    Function to element wise add values in columns
    between two data frame objects.

    Parameters:
    ----------
    df_first: Pandas DataFrame
        The data to add
    df_second: Pandas DataFrame
        The data to add
    cols: list
        The list of columns to add
    index_col_name: str
        The name of a column to sort the data by and then add them.
        To ensure correct row wise subtraction.
    """

    # Sort the values before subtracting
    df_first = df_first.sort_values(by=index_col_name).set_index(index_col_name)
    df_second = df_second.sort_values(by=index_col_name).set_index(index_col_name)

    df_subtracted = df_first.copy()

    for col in cols:
        if col in df_second and col in df_first:
            df_subtracted[col] = df_first[col] + df_second[col]
        else:
            df_subtracted[col] = 0

    return df_subtracted.reset_index()

def replace_negatives(x):
    """
    Simple function to be used by Pandas applymap function
    to replaces negative values in the data elements
    """

    
    if type(x) == type(''):
        return x
    if x < 0:
        return 0
    else:
        return x

def get_unique_id(df, cols_to_add, col_name, index=0):
   """
   Helper function to create a unique id for a dataframe using concatenation of strings
   Parameters:
  -----------
       df: Dataframe to create unique id
       cols_to_add: list
       Column values to concatenate
       col_name: str
       Name of the column to be displayed
       index: Default 0
       At which index, the new column needs to be inserted
   Returns:
  -------
   Dataframe with the unique id column
   """
   # Creating an Unique id column with an empty string
   df.insert(index, col_name, ' ')
   for col in cols_to_add:
       # Converting any datatype to string
       df = df.astype({
           col: 'string'
       })
       df[col_name] = df[col_name] + df[col]
   # After concatenating removing the whitespaces
   df[col_name].str.strip()

   return df
