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


def subject_grouping_v2(df, subject_group, sub_mark):
    """
    Function to extract 12th subject-wise student level data.
    The dataframe consists multiple subjects in the same column
    Function to make subject names or subject_group as column headers
    and the corresponding mark as the row values

    Parameters:
    ----------
        df: Dataframe to group the subjects
        subject_group: dict
        For Example: {
        "others_group": ["BIO-CHEMISTRY", "MICRO-BIOLOGY"]
        Subject group and the list of subjects belongs to the group
        sub_mark: dict
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
                if sub_group == "subjects_of_focus":
                    updated_sub_df[sub] = updated_sub_df[mark]
                    sub_df = pd.concat([sub_df, updated_sub_df])
                    print("SUBJECT GROUP: ", sub_group)
                    print(sub_df)
                # Or assign a new column with the subject group name and their corresponding mark as the column value
                else:
                    updated_sub_df[sub_group] = updated_sub_df[mark]
                    sub_df = pd.concat([sub_df, updated_sub_df])
                    print(sub_group)
                    print(sub_df)
            if sub_group == "subjects_of_focus":
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

def get_grouping_level_data(df_dict, subject_group, sub_mark, grouping_levels, agg_dict, col_name_to_concat, filter_dict):
    """
    Function to group student level data for different management types and build
    a consolidated dataframe. Additionally, data is grouped with the given grouping level
    minus the management type to get aggregated data at 'all management' level.

    For example, grouping levels can be ['District', 'Block', 'management'].
    The function will group and return data as:
        district A | Block i | Govt | aggregated data
        district A | Block i | Aided | aggregated data
        .
        .
        district A | Block i | All Management | aggregated data
        district A | Block ii | Govt | aggregated data
        .
        .

    Parameters:
    ----------
    df_dict: dict
        Management type - student data key-value pairs
    subject_group: dict
        Subject group name and the list of subjects belongs to the group
        For Example: {
            "others_group": ["BIO-CHEMISTRY", "MICRO-BIOLOGY"]
        }
    sub_mark: dict
        Subject name column and their corresponding mark column
        For Example:
            "sub_mark": {
                "SUBNAME_B3": "BMARK3",
                "SUBNAME_B4": "BMARK4",
                "SUBNAME_B5": "BMARK5",
                "SUBNAME_B6": "BMARK6"
            }
    agg_dict: dict
        For Example:
            "agg_dict": {
                "cols.tot_stu": "count",
                "cols.stu_pass": "sum",
                "cols.lang_marks": "median",
                "cols.eng_marks": "median"
            }
    grouping_levels: list
        For Example to group at a block level: ["cols.district_name", "cols.block_name", "cols.management"]
    col_name_to_concat: str
        To concatenate new string value to the aggregate columns
        For Example: 'curr_yr'

    Returns:
    -------
    Grouped consolidated data frame
    """

    # Creating an empty dataframe
    df_master = pd.DataFrame()

    # Values to be excluded in the dataframe
    values_to_exclude = ['AAA', 'XXX', 'DELETED']

    # For each school management type dataframe grouping at a given grouping level
    for management_type, df in df_dict.items():

        # Data cleaning - excluding invalid values from the dataframe
        df = utilities.filter_dataframe(df, filter_dict, include=True)

        # For each management type getting student level data subject-wise
        sub_group_df = subject_grouping_v2(df, subject_group, sub_mark)
        print(sub_group_df)
        # Concatenating each management type dataframe into a single master dataframe
        # df_master is to be used afterwards for grouping to 'all management' level
        df_master = pd.concat([df_master, df])
        # Grouping each management type df at a given grouping level
        df = utilities.group_agg_rename(df, grouping_levels, agg_dict, col_name_to_concat)
        for sub, sub_df in sub_group_df.items():
            try:
                sub_df = utilities.group_agg_rename(sub_df, grouping_levels, {sub: "median", sub: "std"}, col_name_to_concat)
                sub_df.update({sub: sub_df})
                df = df.merge(sub_df, how='left', on=grouping_levels)
            except KeyError:
                continue
        # Replace student level data with grouped data in dictionary
        df_dict.update({management_type: df})

    # Consolidate grouped data for each management type into a single dataframe
    merged_df = pd.concat(df_dict.values())

    # Rename values in previously built df_master for the column management type to 'all management'
    # To help in grouping to all management level
    df_master[cols.management] = cols.all_management
    dir_path = file_utilities.get_curr_month_gen_reports_dir_path()
    file_utilities.save_to_excel({"Report": df_master}, "12th_stu_lvl_sub_v1.xlsx", dir_path=dir_path)

    sub_group_df = subject_grouping_v2(df_master, subject_group, sub_mark)
    # Group and aggregate on this data
    df_master = utilities.group_agg_rename(df_master, grouping_levels, agg_dict, col_name_to_concat)
    for sub, sub_df in sub_group_df.items():
        try:
            sub_df = utilities.group_agg_rename(sub_df, grouping_levels, {sub: "median", sub: "std"},
                                                col_name_to_concat)
            sub_df.update({sub: sub_df})
            df_master = df_master.merge(sub_df, how='left', on=grouping_levels)
        except KeyError:
            continue
    dir_path = file_utilities.get_curr_month_gen_reports_dir_path()
    file_utilities.save_to_excel({"Report": curr_ac_yr_schl_lvl}, "12th_sch_lvl_sub_v1.xlsx", dir_path=dir_path)
    # Concatenate 'all management' grouped data and management type consolidated grouped data
    df_master = pd.concat([df_master, merged_df])

    return df_master


def subject_grouping(df, subject_group, sub_mark):
    """
    Function to extract 12th subject-wise student level data.

    Parameters:
    ----------
        df: Dataframe to group the subjects
        subject_group: dict
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
    prev_ac_yr_schl_lvl[cols.prev_avg_marks] = round((prev_ac_yr_schl_lvl[cols.prev_tot_marks] / 6), 2)
    # Deleting the unnecessary columns
    prev_ac_yr_schl_lvl.drop(columns=[cols.prev_pass, cols.prev_tot_stu, cols.prev_tot_marks], inplace=True)

    # Getting the Pass % at a school level for current academic year
    curr_ac_yr_schl_lvl[cols.curr_pass_perc] = round(
        ((curr_ac_yr_schl_lvl[cols.curr_pass] / curr_ac_yr_schl_lvl[cols.curr_tot_stu]) * 100), 2)

    # Add the average median marks at school level
    curr_ac_yr_schl_lvl[cols.curr_avg_marks] = round((curr_ac_yr_schl_lvl[cols.curr_tot_marks] / 6), 2)

    # Deleting the unnecessary columns
    curr_ac_yr_schl_lvl.drop(columns=[cols.curr_tot_marks], inplace=True)

    #dir_path = file_utilities.get_curr_month_gen_reports_dir_path()
    #file_utilities.save_to_excel({"Report": curr_ac_yr_schl_lvl}, "12th_sch_lvl_sub_v1.xlsx", dir_path=dir_path)

def data_prep(subject_group_config, metric_report_config):
    """
    Function to call the internal functions
    Args:
        subject_group_config:
        metric_source_config:

    Returns:

    """
    # Get the source data configuration for the report code
    source_config = metric_report_config['source_config_curr_yr']
    # Reading the Excel files as a dict
    df_data_set = data_fetcher.get_data_set_from_config(source_config, "miscellaneous_configs")
    # Get the subject group config
    subject_group = subject_group_config['subjects']
    sub_mark = subject_group_config['sub_mark']
    filter_dict = metric_report_config['filter_dict']
    # Get the group levels from the config
    grouping_levels = metric_report_config['grouping_levels']
    state_grouping_levels = grouping_levels['state_grouping_levels']
    agg_dict = metric_report_config['agg_dict']
    get_grouping_level_data(df_data_set, subject_group, sub_mark, state_grouping_levels,agg_dict, 'curr_yr', filter_dict)


if __name__ == "__main__":
    subject_group_config = config_reader.get_config("12TH_SUBJECTS_GROUPING", "miscellaneous_configs")
    subject_group_config = cols.update_nested_dictionaries(subject_group_config)
    metric_report_config = config_reader.get_config("12th_board_block_level_report", "miscellaneous_configs")
    metric_report_config = cols.update_nested_dictionaries(metric_report_config)
    data_prep(subject_group_config, metric_report_config)