"""
Module to create a report of user details and their selected answers for the quiz.
"""
import sys

sys.path.append('../')

import pandas as pd
import utilities.dbutilities as dbutilities
import utilities.file_utilities as file_utilities

def qstn_list_fetch(qset_id:list, credentials_dict:dict):
    """
    Function to fetch the list of questions id for the given quiz id (qset_id)

    Parameters:
    ----------
    qset_id: list
        quiz_set_id for the quiz

    credentials_dict:dict
        db credentials

    Returns:
    -------
    List of question_id for the given question id (qset_id)
    """

    df = dbutilities.fetch_data_as_df(credentials_dict, 'Quiz_qstn_list.sql', qset_id)
    qstn_lst = [df._get_value(0, 'question_ids_list')]
    return qstn_lst



def qstn_ans_fetch(qstn_lst:list, credentials_dict:dict):
    """
    Function to fetch the list of questions text,answers,choice for the given list of question-ids
    Parameters:
    ----------
    qstn_lst: list
        List of questions for the defined qset_id

    credentials_dict:dict
        db credentials

    Returns:
    -------
    The dataframe with answer and correct choices for each question-ids
    """

    df = dbutilities.fetch_data_as_df(credentials_dict, 'Quiz_qstn_ans_text.sql', qstn_lst)
    return df

def user_selected_answers_fetch(qset_id:list, credentials_dict:dict):
    """
    Function to fetch the user selected answers with user detials
    Parameters:
    ----------
    qset_id: list
        quiz id for the quiz

    credentials_dict:dict
        db credentials

    Returns:
    -------
    The dataframe with user details and their answers
    """

    df = dbutilities.fetch_data_as_df(credentials_dict, 'Quiz_teacher_detials_with_answers.sql', qset_id)
    return df

def process_qstn_ans(qstn_ans:pd.DataFrame):
    """
    Function to prepare the dataframe with question and answer for merging
    Parameters:
    __________
    qstn_ans: :pd.DataFrame
       Data frame with question and answer details

    Returns:
    ________
    The data frame with choice string, answers, choices processed for merging

    """
    # Concatenate question_id with choice_id to get question id - choice id string
    qstn_ans['choice_strng'] = qstn_ans['q_id'].astype(str) + qstn_ans['choice_id'].astype(str)
    qstn_ans['choice_strng'] = qstn_ans['choice_strng'].astype(int)

    # Dropping the columns not required while merging
    qstn_ans.drop(columns=['Questions', 'choice_id', 'q_id'], axis=1, inplace=True)
    return qstn_ans

def process_usa(usa:pd.DataFrame, questions_list:list):
    """
    Function to prepare the dataframe with question and answer for merging
    Parameters:
    __________
    usa:pd.DataFrame
       Data frame with user details and their selected answers

    questions_list:list
       Unique questions list
    Returns:
    ________
    The data frame with user detials and the questions text as columns processed for merging

    """
    usa.sort_values('AnswerString')
    # splitting comma separated values
    usa[questions_list] = usa.AnswerString.str.split(',', expand=True)
    usa[questions_list] = usa[questions_list].astype(int)

    # dropping the columns not required
    usa.drop(columns=['AnswerString'], axis=1, inplace=True)
    return usa


def get_quiz_report(qstn_ans: pd.DataFrame, usa: pd.DataFrame, questions_list: list, no_of_questions: int):

    """
    Parameters:
    ----------
    qstn_ans: pd.DataFrame
        Pre processed data frame with question and answer

    usa: pd.DataFrame
        Pre processed data frame with user details and their selected answers

    questions_list: list
        Unique questions list

    no_of_questions: int
        Number of unique questions

    Returns:
    --------
        The data frame with user selected answers and their marks in readable format
    """
    for i in range(no_of_questions):
        question = questions_list[i]
        answer_choice = question + "_ans"
        correct = question + "_correct"

        # To rename columns for merging
        qstn_ans = qstn_ans.rename(columns={
            qstn_ans.columns[2]: question,
            qstn_ans.columns[1]: correct,
            qstn_ans.columns[0]: answer_choice
        })
        usa = pd.merge(usa, qstn_ans, how='left', on=question)
    usa.drop(columns=questions_list, axis=1, inplace=True)

    # returns the df with user selected answers and their marks
    return usa

def main():
    """
    To generate the report for a specific quiz ID containing user details with their
    selected answers in a readable format .

    """

    # Edit the two lines below for each quiz report
    # To create the report for the defined quiz_id
    qset_id = [30256]
    report_name = '30256_9_10'

    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Fetch the list of question ids
    qstn_lists = qstn_list_fetch(qset_id, credentials_dict)

    # Fetch question and answer details for the list of question ids
    qstn_ans = qstn_ans_fetch(qstn_lists, credentials_dict)

    # Get user selected answers for the list of questions ids
    usa = user_selected_answers_fetch(qset_id, credentials_dict)

    # Get the list of unique questions
    questions_list = qstn_ans['Questions'].unique()

    # Get number of questions
    no_of_questions = qstn_ans['Questions'].nunique()

    # Prepare questions and answers detail for merge with user answers
    process_qstn_ans(qstn_ans)

    # Prepare user selected answers for merge with questions
    process_usa(usa, questions_list)

    # Get human-readable quiz report
    quiz_report = get_quiz_report(qstn_ans, usa, questions_list, no_of_questions)

    # Save report
    # Get the current directory path to save the report
    directory_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('TPD_quiz_data')
    file_utilities.save_to_excel({'Report': quiz_report}, report_name+'.xlsx', dir_path=directory_path)


if __name__ == "__main__":
    main()

