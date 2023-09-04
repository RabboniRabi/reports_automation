import sys
sys.path.append('../')

import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import data_cleaning.column_cleaner as column_cleaner
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols
import pandas as pd
import utilities.report_splitter_utilities as report_splitter


def subject_grouping(df, subject_group, sub_mark):
    """
    Function to extract 12th subject-wise student level data.

    Parameters:
    ----------
        df: Dataframe to group the subjects
        subject_group: Dict
        For Example: {
        "others_group": ["BIO-CHEMISTRY", "MICRO-BIOLOGY"]
        Subject group and the list of subjects belongs to the group
        sub_mark: Dict
        Subject name column and their corresponding mark column
    Returns:
    Subject-wise student data as a dictionary
    """
    # Creating an empty dictionary to store the subject, subject_group dataframes
    final_sub_dict = dict()
    group_dict = dict()
    for sub_group, subjects in subject_group.items():
        for sub in subjects:
            # Creating an empty dataframe to filter each subjects
            sub_df = pd.DataFrame()
            for sub_name, mark in sub_mark.items():
                # Filtering the dataframe for the respective subject name
                updated_sub_df = df[df[sub_name] == sub]
                # If subject_group is main_group assigning a new column with the subject name and their corresponding mark as the column value
                if sub_group == "main_group":
                    updated_sub_df[sub] = updated_sub_df[mark]
                    sub_df = pd.concat([sub_df, updated_sub_df])
                # Or assign a new column with the subject group name and their corresponding mark as the column value
                else:
                    updated_sub_df[sub_group] = updated_sub_df[mark]
                    sub_df = pd.concat([sub_df, updated_sub_df])
            if sub_group == "main_group":
                # Updating in the master dictionary
                final_sub_dict.update({sub: sub_df})
            else:
                # For arts, vocational, and others updating it another dictionary
                group_dict.update({sub: sub_df})
            # After updating, deleting the dataframe
            del sub_df

    for sub_group in subject_group.keys():
        # Creating an empty dataframe to extract all the group_subjects as a dataframe
        group_df = pd.DataFrame()
        for sub, df in group_dict.items():
            # Checking if the subject in subject_group's list of subjects.
            # Basically combining multiple subject dataframe to a single subject group (vocational group and so on) dataframe
            if sub in subject_group[sub_group]:
                group_df = pd.concat([group_df, df])
            else:
                continue
        # Dropping the duplicates in the whole dataframe
        group_df.drop_duplicates(inplace=True, ignore_index=True)
        # Updating it in the master dictionary
        final_sub_dict.update({sub_group: group_df})
        # After updating, deleting the dataframe
        del group_df
    return final_sub_dict
def get_school_level_data(df_master, sub_group, grouping_levels, agg_dict, col_name_to_concat):
    """
    Function to group the student level data at a school level
    Parameters:
    ----------
        df_master: master dataframe to with all the subjects and student level information
        sub_group: Dataframe with the respective subjects in a dictionary
        agg_dict: Dict
        For Example:
            "agg_dict": {
                "cols.tot_stu": "count",
                "cols.stu_pass": "sum",
                "cols.lang_marks": "median",
                "cols.eng_marks": "median"
            }
        grouping_levels: list
        col_name_to_concat: str
    Returns:
    School level dataframe
    """
    # Till eng, group the dataframe to school level and consider it as master dataframe
    df_master = utilities.group_agg_rename(df_master, grouping_levels, agg_dict, col_name_to_concat)
    print(df_master.columns)
    # For each subject dataframe grouping at a school level and merging this dataframe to master dataframe
    for sub, df in sub_group.items():
        try:
            df = utilities.group_agg_rename(df, grouping_levels, {sub: "median"}, col_name_to_concat)
            sub_group.update({sub: df})
            df_master = df_master.merge(df, how='left', on=grouping_levels)
        except KeyError:
            continue
    return df_master
def get_prepped_data_for_analysis(report_config):
    """
    Function to prepare the 12th board results data for analysis

    Parameters:
    ----------
    report_config: dict
        The configuration containing variable values that will be used to prepare the data

    Returns:
    --------
    Data prepared as a data frame object
    """
    # Get the source data configuration for the report code
    source_config = report_config['source_config']
    # Reading the Excel files as a dict
    df_data_set = data_fetcher.get_data_set_from_config(source_config, "miscellaneous_configs")
    # Getting previous academic year and current academic year as a separate dataframe
    prev_ac_yr_raw_data, curr_ac_yr_raw_data = df_data_set["prev_yr_data"], df_data_set["curr_yr_data"]

    # Rename the column names to standard format
    prev_ac_yr_raw_data = column_cleaner.standardise_column_names(prev_ac_yr_raw_data)
    curr_ac_yr_raw_data = column_cleaner.standardise_column_names(curr_ac_yr_raw_data)

    # Getting the subject grouping
    subject_group = report_config['subjects']
    sub_mark = report_config['sub_mark']
    # For the previous and current year getting student level data subject-wise
    sub_lvl_stu_prev_yr = subject_grouping(prev_ac_yr_raw_data, subject_group, sub_mark)
    sub_lvl_stu_curr_yr = subject_grouping(curr_ac_yr_raw_data, subject_group, sub_mark)

    # Getting grouping levels and columns to aggregate information from the json
    grouping_levels = report_config['grouping_levels']
    agg_dict = report_config['agg_dict']

    # Grouping the current academic year student level data to school level
    prev_ac_yr_schl_lvl = get_school_level_data(prev_ac_yr_raw_data, sub_lvl_stu_prev_yr, grouping_levels, agg_dict, 'prv_yr')
    curr_ac_yr_schl_lvl = get_school_level_data(curr_ac_yr_raw_data, sub_lvl_stu_curr_yr, grouping_levels, agg_dict, 'curr_yr')

    # Getting the pass % at a school level for previous academic year
    prev_ac_yr_schl_lvl[cols.prev_pass_perc] = round(
        ((prev_ac_yr_schl_lvl[cols.prev_pass] / prev_ac_yr_schl_lvl[cols.prev_tot_stu]) * 100), 2)

    # Add the average median marks at school level
    prev_ac_yr_schl_lvl[cols.prev_avg_marks] = round((prev_ac_yr_schl_lvl[cols.prev_tot_marks] / 5), 2)
    # Deleting the unnecessary columns
    prev_ac_yr_schl_lvl.drop(columns=[cols.prev_pass, cols.prev_tot_stu, cols.prev_tot_marks], inplace=True)

    # Getting the Pass % at a school level for current academic year
    curr_ac_yr_schl_lvl[cols.curr_pass_perc] = round(
        ((curr_ac_yr_schl_lvl[cols.curr_pass] / curr_ac_yr_schl_lvl[cols.curr_tot_stu]) * 100), 2)

    # Add the average median marks at school level
    curr_ac_yr_schl_lvl[cols.curr_avg_marks] = round((curr_ac_yr_schl_lvl[cols.curr_tot_marks] / 5), 2)

    # Deleting the unnecessary columns
    curr_ac_yr_schl_lvl.drop(columns=[cols.curr_tot_marks], inplace=True)

    #dir_path = file_utilities.get_curr_month_gen_reports_dir_path()
    #file_utilities.save_to_excel({"Report": curr_ac_yr_schl_lvl}, "12th_sch_lvl_sub_v1.xlsx", dir_path=dir_path)

if __name__ == "__main__":
    config = config_reader.get_config('12th_board_dist_lvl_report_card', 'miscellaneous_configs')
    config = cols.update_nested_dictionaries(config)
    get_prepped_data_for_analysis(config)