"""
Code to rank the districts based on average marks scored on 10th to provide a state overview and also district overview
"""
import sys
sys.path.append('../')
import pandas as pd
import utilities.column_names_utilities as cols
import utilities.dbutilities as dbutilities
import data_cleaning.column_cleaner as column_cleaner
import utilities.file_utilities as file_utilities
import utilities.report_splitter_utilities as report_splitter
import xlsxwriter


def colour_coding(average_marks):
    """
    Function to format the cells based on a criteria
    Args:
        average_marks: column to grade

    Returns:
    Formatted data
    """

    red = 'background-color: red;'
    orange = 'background-color: orange;'
    yellow = 'background-color: yellow;'
    green = 'background-color: green;'
    default = ''
    if average_marks <= 35 or (average_marks == "Poor"):
        return red
    elif((average_marks > 35) and (average_marks <= 50)) or (average_marks == "Needs Improvement"):
        return orange
    elif ((average_marks > 50) and (average_marks <= 70)) or (average_marks == "Satisfactory"):
        return yellow
    elif average_marks > 70:
        return green
    else:
        return default

def _get_overall_school_performance(average_marks):
    """
    Function to get overall school performance based on average marks.
    Args:
        average_marks: column to grade

    Returns:
    School-wise performance data
    """
    if average_marks <= 35:
        return "Poor"
    elif(average_marks > 35) and (average_marks <= 50):
        return "Needs Improvement"
    elif (average_marks > 50) and (average_marks <= 70):
        return "Satisfactory"
    else:
        return "Good"

def district_level_ranking(df, rank_dist_columns):
    """
    Function to rank the data district-wise
    Args:
        data_dict: Pandas Dataframe
            Dataframe to rank district-wise

    """
    # Splitting the data based on district
    data_dict = report_splitter.split_report(df, cols.district_name)

    # Loop to iterate through the dictionary to rank the data district-wise
    for dist, df in data_dict.items():
        # Finding the total number of schools in the district since rank should look like 15/175
        dist_total_schools = df[cols.udise_col].nunique()
        # Loop to iterate to sort the columns
        for rank_col in rank_dist_columns.keys():
            # Sorting the dataframe based on average marks, subject-wise average marks
            df.sort_values(by=rank_col, ascending=False, inplace=True)
            index = df.columns.get_loc(rank_col) + 2
            # Ranking district-wise
            df.insert(index, rank_dist_columns[rank_col], range(1, 1 + len(df)))
            df[rank_dist_columns[rank_col]] = df[rank_dist_columns[rank_col]].apply(lambda rank_dist: str(rank_dist) + '/' + str(dist_total_schools))

        # Deleting the district column
        df.drop(columns=cols.district_name, inplace=True)

        # Updating the ranked dataframe to the corresponding district in the dictionary
        data_dict.update({dist: df})

        # Deleting the dataframe after updating.
        del df
    # Saving the district-wise ranked data
    report_splitter.save_split_report(data_dict, "10th_average_marks")


def state_level_ranking(df, rank_state_columns):
    """
    Function to rank the data State-wise
    Args:
        df: Dataframe to rank
        sort_columns: list
            columns to sort
        rank_state_columns: list


    Returns:
    State level ranked dataframe
    """
    # Get the school performance based on average marks
    index = df.columns.get_loc(cols.average_marks) + 1
    df.insert(index, cols.school_performance, df[cols.average_marks].apply(_get_overall_school_performance))

    # Finding the total number of schools in the state since rank should look like 15/6250
    state_total_schools = df[cols.udise_col].nunique()

    # Loop to iterate to sort the columns
    for rank_col_value, rank_col_name in rank_state_columns.items():
        # Sorting the dataframe based on average marks, subject-wise average marks
        df.sort_values(by=rank_col_value, ascending=False, inplace=True)
        index = df.columns.get_loc(rank_col_value) + 1
        # Ranking state-wise
        df.insert(index, rank_col_name, range(1, 1 + len(df)))
        df[rank_col_name] = df[rank_col_name].apply(lambda rank_state: str(rank_state) + '/' + str(state_total_schools))



    # Reordering the columns for better readability
    #df = df.iloc[:, [6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 0, 15, 1, 16, 2, 17, 3, 18, 4, 19, 5]]


    return df


def main():
    """
    Function to call the internal function
    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials_rabboni.json')

    # Get the 10th government school average marks for the accademic year 2022-23 from the database as a Pandas DataFrame object
    raw_data_23 = dbutilities.fetch_data_as_df(credentials_dict, 'sslc_govt_school_avg_marks.sql')
    # Get the 10th government school average marks for the accademic year 2021-22 from the database as a Pandas DataFrame object
    raw_data_22 = dbutilities.fetch_data_as_df(credentials_dict, 'prev_yr_sslc_govt_school_avg_marks.sql')
    raw_data = raw_data_23.merge(raw_data_22, how='left', on=[cols.district_name, cols.block_name, cols.udise_col, cols.school_name])
    # Rename the column names to standard format
    raw_data = column_cleaner.standardise_column_names(raw_data)


    # Declaring what column to sort and ranking column names
    rank_state_columns = {
        cols.average_marks: cols.rank_state,
        cols.lang_average_marks: cols.lang_rank_state,
        cols.eng_average_marks: cols.eng_rank_state,
        cols.math_average_marks: cols.math_rank_state,
        cols.science_average_marks: cols.science_rank_state,
        cols.social_average_marks: cols.social_rank_state}
    rank_dist_columns = {
        cols.average_marks: cols.rank_dist,
        cols.lang_average_marks: cols.lang_rank_dist,
        cols.eng_average_marks: cols.eng_rank_dist,
        cols.math_average_marks: cols.math_rank_dist,
        cols.science_average_marks: cols.science_rank_dist,
        cols.social_average_marks: cols.social_rank_dist}

    # Get the State level ranking
    df = state_level_ranking(raw_data, rank_state_columns)
    # Get district level ranking
    district_level_ranking(df, rank_dist_columns)

if __name__ == "__main__":
    main()
