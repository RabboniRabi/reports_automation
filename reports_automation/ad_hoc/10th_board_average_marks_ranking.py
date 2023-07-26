"""
Code to rank the districts based on average marks scored on 10th to provide a state overview and also district reports
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

sort_columns = [cols.average_marks, cols.lang_average_marks, cols.eng_average_marks, cols.math_average_marks,
                cols.science_average_marks, cols.social_average_marks]
rank_state_column_names = [cols.rank_state, cols.lang_rank_state, cols.eng_rank_state, cols.math_rank_state,
                     cols.science_rank_state, cols.social_rank_state]
rank_dist_columns = [cols.rank_dist, cols.lang_rank_dist, cols.eng_rank_dist, cols.math_rank_dist,
                     cols.science_rank_dist, cols.social_rank_dist]

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

def district_level_ranking(df):
    """
    Function to rank the data district-wise
    Args:
        data_dict: Pandas Dataframe
            Dataframe to rank district-wise

    """
    # Splitting the data based on district
    data_dict = report_splitter.split_report(df, cols.district_name)

    # Loop to iterate through the dictionary to rank the data district-wise
    for dist in data_dict.keys():
        df = data_dict[dist]
        # Finding the total number of schools in the district since rank should look like 15/175
        dist_total_schools = df[cols.udise_col].nunique()
        count = 0
        # Loop to iterate to sort the columns
        for sort_col in sort_columns:
            # Sorting the dataframe based on average marks, subject-wise average marks
            df.sort_values(by=sort_col, ascending=False, inplace=True)
            # Ranking district-wise
            df.insert(count, rank_dist_columns[count], range(1, 1 + len(df)))
            df[rank_dist_columns[count]] = df[rank_dist_columns[count]].apply(lambda rank_dist: str(rank_dist) + '/' + str(dist_total_schools))
            # Updating the ranked dataframe to the corresponding district in the dictionary
            data_dict.update({dist: df})
            count = count + 1
        # Deleting the dataframe after updating.
        del df
    # Saving the district-wise ranked data
    report_splitter.save_split_report(data_dict, "10th_average_marks")


def state_level_ranking(df):
    """
    Function to rank the data State-wise
    Args:
        df: Dataframe to rank

    Returns:
    State level ranked dataframe
    """

    # Finding the total number of schools in the state since rank should look like 15/6250
    state_total_schools = df[cols.udise_col].nunique()
    count = 0
    # Loop to iterate to sort the columns
    for sort_col in sort_columns:
        # Sorting the dataframe based on average marks, subject-wise average marks
        df.sort_values(by=sort_col, ascending=False, inplace=True)
        # Ranking state-wise
        df.insert(count, rank_state_column_names[count], range(1, 1 + len(df)))
        df[rank_state_column_names[count]] = df[rank_state_column_names[count]].apply(lambda rank_state: str(rank_state) + '/' + str(state_total_schools))
        count = count+1

    # Get the school performance based on average marks
    df[cols.school_performance] = df[cols.average_marks].apply(_get_overall_school_performance)
    # Reordering the columns for better readability
    df = df.iloc[:, [6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 0, 15, 1, 16, 2, 17, 3, 18, 4, 19, 5]]


    return df


def main():
    """
    Function to call the internal function
    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials_rabboni.json')

    # Get the 10th government school average marks from the database as a Pandas DataFrame object
    raw_data = dbutilities.fetch_data_as_df(credentials_dict, 'sslc_govt_school_avg_marks.sql')
    # Rename the column names to standard format
    raw_data = column_cleaner.standardise_column_names(raw_data)
    # Get the State level ranking
    df = state_level_ranking(raw_data)
    district_level_ranking(df)

if __name__ == "__main__":
    main()
