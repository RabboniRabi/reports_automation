"""
Module to create a report of 12th pass out students who have not applied to colleges and
need support - to be used by Career Guidance PMU.
"""

import sys
sys.path.append('../')

import utilities.column_names_utilities as cols
import pandas as pd
import numpy as np


def custom_base_report(df_data_set, merge_sources_configs):
    """
    Custom function to implement the logic to create the ad hoc report

    Parameters:
    ----------
    df_data_set: DataFrame
        dataset as Pandas DataFrame Objects dictionary
    merge_sources_configs: List
        List of configurations to merge the different source datasets together

    Returns:
    -------
    Base report created from source datasets and custom logic
    """

    # Get the HM survey data frame object
    df_hm_survey_data = df_data_set[hm_survey_report]

    """
    Filter out the HM servery data students who:
    - have passed and have applied without college name, but has given doubtful reasons
    - Not applied for college
    - status has not been updated
    """

    # Declare the condition under which a student is considered to have passed
    stu_pass_cond = [(df_hm_survey_data[cols.cg_ex_res_stat] == cols.cg_ex_res_pass)]

    # Declare the condition under which a student is considered to have passed
    # and has applied without college name
    stu_appld_wo_clg_name_cond = [stu_pass_cond & (df_hm_survey_data[cols.cg_stu_appld] == 'Yes') \
                                        & (df_hm_survey_data[cols.cg_clg_nm].isna())]

    # Declare the condition under which a student is considered to have passed
    # and has applied without college name, but has given doubtful reasons
    stu_appld_wo_clg_name_cond_doubtful_cond = [stu_appld_wo_clg_name_cond \
                                            & (df_hm_survey_data[cols.cg_stu_cert].str.contains('10th|11th'))]


    # Declare the condition under which a student is considered to have not applied for college
    stu_not_appld_cond = [stu_pass_cond & (df_hm_survey_data[cols.cg_stu_appld] == 'No')]

    # Declare the condition under which a student's status is considered to be not updated
    stu_stat_not_updtd_cond = [stu_pass_cond & (df_hm_survey_data[cols.cg_stu_appld] == 'Not updated')]

    # Declare the condition under which a student is considered a target
    stu_target_cond = [stu_appld_wo_clg_name_cond_doubtful_cond | stu_not_appld_cond | stu_stat_not_updtd_cond]

    # Declare the true condition value to be filled.
    # In this case, there is only one overall condition being met (not different criteria)
    choices = [True]

    # Add a column to the data indicating if the student has applied without college name, but has given doubtful reasons
    df_hm_survey_data[cols.cg_stu_appld_wo_clg_name_dbt] = np.select(stu_appld_wo_clg_name_cond_doubtful_cond, \
                                                            choices, default=False)

    # Add a column to the data indicating if student has not applied
    df_hm_survey_data[cols.cg_stu_not_appld] = np.select(stu_not_appld_cond, choices, default=False)

    # Add a column to the data indicating if student status has not been updated
    df_hm_survey_data[cols.cg_stu_not_updtd] = np.select(stu_stat_not_updtd_cond, choices, default=False)

    # Add a column to the data indicating if student is a traget for volunteer survey
    df_hm_survey_data[cols.cg_stu_tgt]= np.select(stu_target_cond, choices, default=False)

    # Get the volunteer survey data object
    df_vol_survey_data = df_data_set[volunteer_survey_report]

    # Get a subset of data
    df_vol_survey_data = df_vol_survey_data[[cols.cg_stu_emis_no, cols.cg_stu_not_appld_reason, cols.cg_stu_supp_req]]

    # Get the volunteer dataset merge configuration
    vol_merge_config = merge_sources_configs[0]

    # Merge the HM survey data with the reasons and support required values in the volunteer survey report
    df_merged = df_hm_survey_data.merge(df_vol_survey_data, how=vol_merge_config['merge_type'], on=vol_merge_config['join_on'])

    return df_merged

    