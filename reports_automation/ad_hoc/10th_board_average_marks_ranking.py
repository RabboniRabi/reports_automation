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
def colour_coding(average_marks):

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
    if average_marks <= 35:
        return "Poor"
    elif(average_marks > 35) and (average_marks <= 50):
        return "Needs Improvement"
    elif (average_marks > 50) and (average_marks <= 70):
        return "Satisfactory"
    else:
        return "Good"

def state_level_ranking(df):
    """
    Function to rank the data State-wise
    Args:
        df: Dataframe to rank

    Returns:

    """
    # Sorting the dataframe based on average marks.
    df.sort_values(by=cols.average_marks, ascending=False, inplace= True)
    # Finding the total number of unique values in a column since rank should look like 15/6250
    state_total = df[cols.district_name].nunique()
    df.insert(0, cols.rank_state, range(1, 1 + len(df)))
    df.reset_index(inplace=True)
    df[cols.school_performance] = df[cols.average_marks].apply(_get_overall_school_performance)
    df.style.apply(colour_coding, subset=["lang_average_marks", "eng_average_marks", "math_average_marks", "science_average_marks", "social_average_marks"], axis=0)
    data_dict = report_splitter.split_report(df, cols.district_name)
    report_splitter.save(data_dict)
    print(df)

def main():
    """
    Function to call the internal function
    Returns:

    """
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the 10th government school average marks from the database as a Pandas DataFrame object
    raw_data = dbutilities.fetch_data_as_df(credentials_dict, 'sslc_govt_school_avg_marks.sql')
    # Get the State level ranking
    state_level_ranking(raw_data)

main()