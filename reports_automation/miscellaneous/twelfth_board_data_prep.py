import sys
sys.path.append('../')

import readers.config_reader_v2 as config_reader
import readers.data_fetcher_v2 as data_fetcher
import data_cleaning.column_cleaner as column_cleaner
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols
import pandas as pd
import utilities.report_splitter_utilities as report_splitter

def subject_grouping(df, major_subject_grouping, minor_sub_grouping):
    """
    Function to extract 12th subject-wise student level data.
    Args:
        df:
        major_subject_grouping:

    Returns:
    Subject-wise student data as a dictionary
    """
    # Creating an empty dictionary
    subjects = dict()
    for sub, mark_group in major_subject_grouping.items():
        # Creating an empty dataframe
        subject_marks = pd.DataFrame()
        for mark in mark_group.keys():
            for group_code in mark_group[mark]:
                # For each mark column checking whether the subject group code is there or not if it's there updating in the dictionary
                updated_sub_df = df[df[cols.group_code] == group_code]
                updated_sub_df[sub] = updated_sub_df[mark]
                # Concatenating the marks each subject
                subject_marks = pd.concat([subject_marks, updated_sub_df])


        # Updating the dictionary with subjects
        subjects.update({sub: subject_marks})
        # After updating deleting the dataframe
        del subject_marks

    for sub, groups in minor_sub_grouping.items():
        # Creating an empty dataframe
        minor_subject_marks = pd.DataFrame()
        for grp_code in groups:

            updated_sub_df = df[df[cols.group_code] == grp_code]
            updated_sub_df[sub] = updated_sub_df[cols.mark_3] + updated_sub_df[cols.mark_4] + updated_sub_df[cols.mark_5] + updated_sub_df[cols.mark_6]
            minor_subject_marks = pd.concat([minor_subject_marks, updated_sub_df])
        # Updating the dictionary with subjects
        subjects.update({sub: minor_subject_marks})
         # After updating deleting the dataframe
        del minor_subject_marks


    #report_splitter.save_split_report(subjects, "12th_subject_grouping")
    return subjects

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
    curr_ac_yr_raw_data = df_data_set["curr_yr_data"]

    # Rename the column names to standard format
    #prev_ac_yr_raw_data = column_cleaner.standardise_column_names(prev_ac_yr_raw_data)
    curr_ac_yr_raw_data = column_cleaner.standardise_column_names(curr_ac_yr_raw_data)

    # Getting the subject grouping
    major_sub_grouping = report_config['main_subjects_grouping']
    minor_sub_grouping = report_config['minor_subject_groupings']

    # Getting grouping levels and columns to aggregate information from the json
    #grouping_levels = report_config['grouping_levels']
    grouping_levels = [cols.district_name, cols.block_name, cols.udise_col, cols.school_name]
    agg_dict = report_config['agg_dict']
    agg_dict = cols.update_nested_dictionaries(agg_dict)

    # Grouping the current academic year student level data to school level
    curr_ac_yr_schl_lvl = utilities.group_agg_rename(curr_ac_yr_raw_data, grouping_levels, agg_dict, 'curr_yr')
    sub_lvl_stu = subject_grouping(curr_ac_yr_raw_data, major_sub_grouping, minor_sub_grouping)
    for sub, df in sub_lvl_stu.items():
        df = utilities.group_agg_rename(df, grouping_levels, {sub: "median"}, 'curr_yr')
        sub_lvl_stu.update({sub: df})
        curr_ac_yr_schl_lvl = curr_ac_yr_schl_lvl.merge(df, how='left', on=grouping_levels)


    dir_path = file_utilities.get_curr_month_gen_reports_dir_path()
    file_utilities.save_to_excel({"Report": curr_ac_yr_schl_lvl}, "12th_sch_lvl.xlsx", dir_path=dir_path)

if __name__ == "__main__":
    config = config_reader.get_config('12th_board_dist_lvl_report_card', 'miscellaneous_configs')
    #config = cols.update_nested_dictionaries(config)
    get_prepped_data_for_analysis(config)