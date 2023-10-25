"""
    Script to generate HSC results at a given grouping level for each metric
"""
import sys

sys.path.append('../')
import pandas as pd
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import data_cleaning.column_cleaner as column_cleaner
import utilities.column_names_utilities as cols
import utilities.utilities as utilities
import  twelfth_board_data_prep
import utilities.file_utilities as file_utilities
import warnings

warnings.filterwarnings('ignore')
def get_state_grouping_level_rpt(df, grouping_level, subject_grouping, agg_dict):
    """
    Helper Function to get state grouping level report for specific metric

    Parameters:
    ----------
        df: Pandas Dataframe
            Dataframe to filter
        grouping_level: list
            Block grouping level list
        subject_grouping: dict
            Subject group and the list of subjects belongs to the group
        agg_dict: dict
            Columns to aggregate
    Returns:
    State Level Report
    """
    # Pre- Requesite - The grouping level should be either management or management, metric
    # Extracting the unique values for the first filter
    filter_values_lvl_one = set(df[grouping_level[0]].to_list())

    # Creating an empty dataframe to store the grouped data
    df_master = pd.DataFrame()

    if len(grouping_level) == 1:
        # Loop to filter each value in filter level one
        for filter_value in filter_values_lvl_one:
            filter_df = df[df[grouping_level[0]] == filter_value]
            # Getting the aggregation for each filter value
            filter_value_df = twelfth_board_data_prep.get_subject_aggregation(filter_df, grouping_level, subject_grouping, agg_dict)
            # Concatenating the filter dataframe (which would basically have one row) to master dataframe
            df_master = pd.concat([df_master, filter_value_df])

    else:
        # Extracting the unique values for the second filter
        filter_values_lvl_two = set(df[grouping_level[1]].to_list())
        # Loop to filter each value in filter level one
        for filter_value in filter_values_lvl_one:
            filter_level_one_df = df[df[grouping_level[0]] == filter_value]
            # Loop to filter each value in filter level two
            for filter_val in filter_values_lvl_two:
                filter_level_two_df = filter_level_one_df[filter_level_one_df[grouping_level[1]] == filter_val]
                # Getting the aggregation for each filter value
                filter_value_df = twelfth_board_data_prep.get_subject_aggregation(filter_level_two_df, grouping_level,
                                                                                     subject_grouping, agg_dict)
                # Concatenating the filter dataframe (that would basically have one row) to master dataframe
                df_master = pd.concat([df_master, filter_value_df])

    return df_master
def get_district_grouping_level_rpt(df, grouping_level, subject_grouping, agg_dict):
    """
    Helper Function to get district grouping level report for specific metric

    Parameters:
    ----------
        df: Pandas Dataframe
            Dataframe to filter
        grouping_level: list
            Block grouping level list
        subject_grouping: dict
            Subject group and the list of subjects belongs to the group
        agg_dict: dict
            Columns to aggregate

    Returns:
    District level Report
    """
    # Creating and empty dataframe to store the grouped data
    df_master = pd.DataFrame()

    # Pre- Requesite - The grouping level should be either district, management or district, management, metric
    # Extracting the unique values for the first filter and second filter
    filter_values_lvl_one = set(df[grouping_level[0]].to_list())
    filter_values_lvl_two = set(df[grouping_level[1]].to_list())

    if len(grouping_level) == 2:
        # Loop to filter each value in filter level one
        for filter_value in filter_values_lvl_one:
            filter_level_one_df = df[df[grouping_level[0]] == filter_value]
            # Loop to filter each value in filter level two
            for filter_values in filter_values_lvl_two:
                filter_level_two_df = filter_level_one_df[filter_level_one_df[grouping_level[1]] == filter_values]
                # Getting the aggregation for each filter value
                filter_value_df = twelfth_board_data_prep.get_subject_aggregation(filter_level_two_df, grouping_level,
                                                                                 subject_grouping, agg_dict)
                # Concatenating the filter dataframe (that would basically have one row) to master dataframe
                df_master = pd.concat([df_master, filter_value_df])
    else:
        # Extracting the unique values for the third filter
        filter_values_lvl_three = set(df[grouping_level[2]].to_list())
        # Loop to filter each value in filter level one
        for filter_value in filter_values_lvl_one:
            filter_level_one_df = df[df[grouping_level[0]] == filter_value]
            # Loop to filter each value in filter level two
            for filter_values in filter_values_lvl_two:
                filter_level_two_df = filter_level_one_df[filter_level_one_df[grouping_level[1]] == filter_values]
                # Loop to filter each value in filter level three
                for filter_val in filter_values_lvl_three:
                    filter_level_three_df = filter_level_two_df[filter_level_two_df[grouping_level[2]] == filter_val]
                    # Getting the aggregation for each filter value
                    filter_value_df = twelfth_board_data_prep.get_subject_aggregation(filter_level_three_df, grouping_level,
                                                                                 subject_grouping, agg_dict)
                    # Concatenating the filter dataframe (that would basically have one row) to master dataframe
                    df_master = pd.concat([df_master, filter_value_df])
    return df_master
def get_block_grouping_level_rpt(df, grouping_level, subject_grouping, agg_dict):
    """
    Helper Function to get block grouping level report for specific metric

    Parameters:
    ----------
        df: Pandas Dataframe
            Dataframe to filter
        grouping_level: list
            Block grouping level list
        subject_grouping: dict
            Subject group and the list of subjects belongs to the group
        agg_dict: dict
            Columns to aggregate
    Returns:
    ----------
    Block level report
    """
    # Creating and empty dataframe to store the grouped data
    df_master = pd.DataFrame()
    # Pre- Requesite - The grouping level should be either district, block, management or district, block, management, metric
    # Extracting the unique values for the first filter, second filter and third filter
    filter_values_lvl_one = set(df[grouping_level[0]].to_list())
    filter_values_lvl_two = set(df[grouping_level[1]].to_list())
    filter_values_lvl_three = set(df[grouping_level[2]].to_list())
    if len(grouping_level) == 3:
        # Loop to filter each value in filter level one
        for filter_value in filter_values_lvl_one:
            filter_level_one_df = df[df[grouping_level[0]] == filter_value]
            # Loop to filter each value in filter level two
            for filter_values in filter_values_lvl_two:
                filter_level_two_df = filter_level_one_df[filter_level_one_df[grouping_level[1]] == filter_values]
                # Loop to filter each value in filter level three
                for filter_val in filter_values_lvl_three:
                    filter_level_three_df = filter_level_two_df[filter_level_two_df[grouping_level[2]] == filter_val]
                    filter_value_df = twelfth_board_data_prep.get_subject_aggregation(filter_level_three_df, grouping_level,
                                                                                 subject_grouping, agg_dict)
                    df_master = pd.concat([df_master, filter_value_df])
    else:
        # Extracting the unique values for the fourth filter
        filter_values_lvl_four = set(df[grouping_level[3]].to_list())
        # Loop to filter each value in filter level one
        for filter_value in filter_values_lvl_one:
            filter_level_one_df = df[df[grouping_level[0]] == filter_value]
            # Loop to filter each value in filter level two
            for filter_values in filter_values_lvl_two:
                filter_level_two_df = filter_level_one_df[filter_level_one_df[grouping_level[1]] == filter_values]
                # Loop to filter each value in filter level three
                for filter_val in filter_values_lvl_three:
                    filter_level_three_df = filter_level_two_df[filter_level_two_df[grouping_level[2]] == filter_val]
                    # Loop to filter each value in filter level four
                    for fourth_filter_val in filter_values_lvl_four:
                        filter_level_four_df = filter_level_three_df[filter_level_three_df[grouping_level[3]] == fourth_filter_val]
                        # Getting the aggregation for each filter value
                        filter_value_df = twelfth_board_data_prep.get_subject_aggregation(filter_level_four_df, grouping_level,
                                                                                 subject_grouping, agg_dict)
                        # Concatenating the filter dataframe (that would basically have one row) to master dataframe
                        df_master = pd.concat([df_master, filter_value_df])
    return df_master

def get_grouping_level_data(df_dict, grouping_level, grouping_level_flag, sub_mark, subject_grouping, agg_dict):
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
        grouping_level: list
            For Example to group at a block level: ["cols.district_name", "cols.block_name", "cols.management"]
        grouping_level_flag: str
            At what level you want to group - State or District or Block
        sub_mark: dict
            Subject name column and their corresponding mark column
        subject_grouping: dict
            Subject group and the list of subjects belongs to the group
            For Example: {
                "others_group": ["BIO-CHEMISTRY", "MICRO-BIOLOGY"]
                }
        agg_dict: dict
            Columns to aggregate
            "agg_dict_median": {
                "common_agg_dict": {
                "cols.tot_stu": "count",
                "cols.stu_pass": "sum"
                },
            "subjects_of_focus": {
                "cols.lang_marks": "median",
                "cols.eng_marks": "median",
            },
            "main_group": "median",
            "arts_group": "median",
            "vocational_group": "median",
            "others_group": "median"
        },

    Returns:
    -------
    Grouped consolidated data frame

    """
    df_master = pd.DataFrame()
    for management_type, df in df_dict.items():
        # Getting subject grouping for each management type
        df = twelfth_board_data_prep.get_subject_grouping(df, sub_mark)

        # Concatenating each management type dataframe into a single master dataframe
        # df_master is to be used afterwards for grouping to 'all management' level
        df_master = pd.concat([df_master, df])
        # Getting total number of students and pass at a given grouping level
        df_common_sub = utilities.group_agg_rename(df, grouping_level, agg_dict['common_agg_dict'])
        # According to the grouping level flag, the necessary grouping level method is called
        if grouping_level_flag == 'State':
            df_all_group = get_state_grouping_level_rpt(df, grouping_level, subject_grouping, agg_dict)
        elif grouping_level_flag == 'District':
            df_all_group = get_district_grouping_level_rpt(df, grouping_level, subject_grouping, agg_dict)
        elif grouping_level_flag == 'Block':
            df_all_group = get_block_grouping_level_rpt(df, grouping_level, subject_grouping, agg_dict)
        # Merging common subjects
        df_all_group = pd.merge(df_common_sub, df_all_group, on=grouping_level, how='left')
        # Replace student level data with grouped data in dictionary
        df_dict.update({management_type: df_all_group})
    # Consolidate grouped data for each management type into a single dataframe
    merged_df = pd.concat(df_dict.values())
    # Rename values in previously built df_master for the column management type to 'all management'
    # To help in grouping to all management level
    df_master[cols.management] = cols.all_management
    # Getting total number of students and pass at a given grouping level
    df_common_master = utilities.group_agg_rename(df_master, grouping_level, agg_dict['common_agg_dict'])
    # According to the grouping level flag, the necessary grouping level method is called
    if grouping_level_flag == 'State':
        df_master = get_state_grouping_level_rpt(df_master, grouping_level, subject_grouping, agg_dict)
    elif grouping_level_flag == 'District':
        df_master = get_district_grouping_level_rpt(df_master, grouping_level, subject_grouping, agg_dict)
    elif grouping_level_flag == 'Block':
        df_master = get_block_grouping_level_rpt(df_master, grouping_level, subject_grouping, agg_dict)

    df_grouped = pd.merge(df_common_master, df_master, on=grouping_level, how='left')
    df_grouped = pd.concat([df_grouped, merged_df])



    return df_grouped

def _get_grouping_lvl_med_sd(df_dict, grouping_level, grouping_level_flag, sub_mark, subject_grouping, median_agg_dict, std_dev_agg_dict):
    """

    Internal helper function to create a report of data grouped to given grouping level
    and median and standard deviation of specified columns calculated and converting the number of
    columns to rows.

    Parameters:
    ----------
        df_dict: dict
            Data as a dictionary of management-type : data
            key value pairs
        grouping_level: list
            Levels to group the data by
        grouping_level_flag: str
            Flag to check whether State or District or Block
        median_agg_dict: dict
            Dictionary to be used to calculate median values for different levels
            of grouped data (state, district, block)
        std_dev_agg_dict: dict
            Dictionary to be used to calculate standard deviation values for different levels
        of grouped data (state, district, block)
        sub_mark: dict
            Subject name column and their corresponding mark column
        subject_grouping: dict
            Subject group and the list of subjects belongs to the group

    Returns:
    --------
    Report for metric at given grouping level

    """

    # Declare the subject column names to un-pivot the data on
    value_vars_list = [cols.lang_marks, cols.eng_marks,	cols.physics,	cols.chemistry,	cols.mathematics, cols.biology,
                       cols.economics,	cols.commerce, cols.computer_science, cols.tot_marks, cols.main_group,
                       cols.arts_group, cols.vocational_group, cols.others_group]
    # Group the data and get the median values
    df_med = get_grouping_level_data(df_dict.copy(), grouping_level, grouping_level_flag, sub_mark, subject_grouping, median_agg_dict)
    print("Got the median")

    df_med.rename(columns={
        cols.emis_no_count: cols.brd_tot_stu_appr,
        cols.pass_sum: cols.brd_tot_stu_pass,
        cols.language_median: cols.lang_marks,
        cols.english_median: cols.eng_marks,
        cols.physics_median: cols.physics,
        cols.chemistry_median: cols.chemistry,
        cols.mathematics_median: cols.mathematics,
        cols.biology_median: cols.biology,
        cols.economics_median: cols.economics,
        cols.commerce_median: cols.commerce,
        cols.comp_sci_median: cols.computer_science,
        cols.main_group_median: cols.main_group,
        cols.arts_group_median: cols.arts_group,
        cols.vocational_group: cols.vocational_group,
        cols.others_group_median: cols.others_group,
        cols.total_median: cols.tot_marks
    }, inplace=True)

    print("Making the subject columns as rows")
    # Melt the subject columns and values into rows with subject and median values
    df_med = pd.melt(df_med, id_vars=grouping_level + [cols.brd_tot_stu_appr, cols.brd_tot_stu_pass],
                     value_vars=value_vars_list, var_name=cols.subject, value_name='median')
    # Group the data and get the standard deviation values
    df_sd = get_grouping_level_data(df_dict.copy(), grouping_level, grouping_level_flag, sub_mark, subject_grouping, std_dev_agg_dict)
    print("Got the standard deviation")
    df_sd.rename(columns={
        cols.emis_no_count: cols.brd_tot_stu_appr,
        cols.pass_sum: cols.brd_tot_stu_pass,
        cols.language_std: cols.lang_marks,
        cols.english_std: cols.eng_marks,
        cols.physics_std: cols.physics,
        cols.chemistry_std: cols.chemistry,
        cols.mathematics_std: cols.mathematics,
        cols.biology_std: cols.biology,
        cols.economics_std: cols.economics,
        cols.commerce_std: cols.commerce,
        cols.comp_sci_std: cols.computer_science,
        cols.main_group_std: cols.main_group,
        cols.arts_group_std: cols.arts_group,
        cols.vocational_group: cols.vocational_group,
        cols.others_group_std: cols.others_group,
        cols.total_std: cols.tot_marks
    }, inplace=True)
    print(df_sd.columns)

    print("Making the subject columns as rows")
    # Melt the subject columns and values into rows with subject and standard deviation values
    df_sd = pd.melt(df_sd, id_vars=grouping_level, value_vars=value_vars_list,
                    var_name=cols.subject, value_name='std_dev')

    print("Merging both the datasets")
    # Merge median and standard deviation value for the grouped data
    df_med_sd = pd.merge(df_med, df_sd, how='inner', on=grouping_level)

    return df_med_sd

def get_metric_subj_wise_med_sd_rpt(metric: str, df_dict_curr_yr: dict, df_dict_prev_yr: dict,
                                    median_agg_dict: dict, std_dev_agg_dict: dict, sub_mark, sub_group):
    """
       Function to generate reports at state, district & block level for a given metric with
       subject wise data aggregated for median and standard deviation for
       current year and previous year data.

       Parameters:
       ---------
       metric: str
           The data analysis metric for which to generate the report for
       df_dict_curr_yr: dict
           Current year data as a dictionary of management-type : data
           key value pairs
       df_dict_prev_yr: dict
           Previous year data as a dictionary of management-type : data
           key value pairs
       median_agg_dict: dict
           Dictionary to be used to calculate median values for different levels
           of grouped data (state, district, block)
       std_dev_agg_dict: dict
           Dictionary to be used to calculate standard deviation values for different levels
           of grouped data (state, district, block)

       Returns:
       --------
       Dictionary of reports at state, district and block level
    """
    curr_yr = utilities.get_curr_year()
    prev_yr = utilities.get_prev_year()

    # Get block level report
    # Grouping level for block level
    block_grouping_lvl = [cols.district_name, cols.block_name, cols.management, metric]
    block_grouping_lvl = list(dict.fromkeys(block_grouping_lvl))

    # Get the report for current year
    print("Getting block level report for current year: ", block_grouping_lvl, " for this metric ", metric)
    blk_curr_yr = _get_grouping_lvl_med_sd(df_dict_curr_yr, block_grouping_lvl, 'Block', sub_mark, sub_group, median_agg_dict, std_dev_agg_dict)
    # Add year column
    blk_curr_yr[cols.year_col] = curr_yr
    
    # Sort the block report
    blk_curr_yr.sort_values(by=block_grouping_lvl, inplace=True)

    print("Getting block level report for prev year: ", block_grouping_lvl, " for this metric ", metric)
    # Get the report for previous year
    blk_prev_yr = _get_grouping_lvl_med_sd(df_dict_prev_yr, block_grouping_lvl, 'Block', sub_mark, sub_group, median_agg_dict, std_dev_agg_dict)
    # Add year column
    blk_prev_yr[cols.year_col] = prev_yr
    # Sort the block report
    blk_prev_yr.sort_values(by=block_grouping_lvl, inplace=True)
    # Concatenate current year and previous year report
    blk_rpt = pd.concat([blk_curr_yr, blk_prev_yr])

    # Get district level report

    # Grouping level for district
    dist_grouping_lvl = [cols.district_name, cols.management, metric]
    dist_grouping_lvl = list(dict.fromkeys(dist_grouping_lvl))

    print("Getting district level report for current year: ", dist_grouping_lvl, " for this metric ", metric)
    # Get the report for current year
    dist_curr_yr = _get_grouping_lvl_med_sd(df_dict_curr_yr, dist_grouping_lvl, 'District', sub_mark, sub_group, median_agg_dict,
                                           std_dev_agg_dict)
    # Add year column
    dist_curr_yr[cols.year_col] = curr_yr
    # Sort the block report
    dist_curr_yr.sort_values(by=dist_grouping_lvl, inplace=True)

    print("Getting district level report for prev year: ", dist_grouping_lvl, " for this metric ", metric)
    # Get the report for previous year
    dist_prev_yr = _get_grouping_lvl_med_sd(df_dict_prev_yr, dist_grouping_lvl, 'District', sub_mark, sub_group, median_agg_dict,
                                           std_dev_agg_dict)
    # Add year column
    dist_prev_yr[cols.year_col] = prev_yr
    # Sort the block report
    dist_prev_yr.sort_values(by=dist_grouping_lvl, inplace=True)
    # Concatenate current year and previous year report
    dist_rpt = pd.concat([dist_curr_yr, dist_prev_yr])

    # Get State level report

    #Grouping level for State
    state_grouping_level = [cols.management, metric]
    state_grouping_level = list(dict.fromkeys(state_grouping_level))

    print("Getting state level report for curr year: ", state_grouping_level, " for this metric ", metric)
    # Get the report for current year
    state_curr_yr = _get_grouping_lvl_med_sd(df_dict_curr_yr, state_grouping_level, 'State', sub_mark, sub_group, median_agg_dict,
                                            std_dev_agg_dict)
    # Add year column
    state_curr_yr[cols.year_col] = curr_yr
    # Sort the block report
    state_curr_yr.sort_values(by=state_grouping_level, inplace=True)

    print("Getting state level report for prev year: ", state_grouping_level, " for this metric ", metric)
    # Get the report for previous year
    state_prev_yr = _get_grouping_lvl_med_sd(df_dict_prev_yr, state_grouping_level, 'State', sub_mark, sub_group, median_agg_dict,
                                            std_dev_agg_dict)
    # Add year column
    state_prev_yr[cols.year_col] = prev_yr
    # Sort the block report
    state_prev_yr.sort_values(by=state_grouping_level, inplace=True)
    # Concatenate current year and previous year report
    state_rpt = pd.concat([state_curr_yr, state_prev_yr])

    df_metric_subj_wise_rpt = {'Block': blk_rpt, 'District': dist_rpt, 'State': state_rpt}

    return df_metric_subj_wise_rpt
def main():
    """
    Internal function to call the other helper funcitons to generate HSC results for each metric

    """
    # Fetch the configuration for creating the reports
    config = config_reader.get_config("12TH_SUBJECTS_GROUPING", "miscellaneous_configs")
    config = cols.update_nested_dictionaries(config)

    # Get the current year and previous year data set for all management types
    source_config_curr_yr = config['source_config_curr_yr']
    df_data_curr_yr = data_fetcher.get_data_set_from_config(source_config_curr_yr, "miscellaneous_configs")

    source_config_prev_yr = config['source_config_prev_yr']
    df_data_prev_yr = data_fetcher.get_data_set_from_config(source_config_prev_yr, "miscellaneous_configs")

    # Data cleaning - Removing junk and invalid entries
    filter_dict = config['filter_dict']


    for management_type, df in df_data_curr_yr.items():
        df = utilities.filter_dataframe(df, filter_dict, include=False)
        df = column_cleaner.standardise_column_names(df)
        df[cols.stu_pass].replace({'P': 1}, inplace=True)
        df_data_curr_yr.update({management_type: df})

    for management_type, df in df_data_prev_yr.items():
        df = utilities.filter_dataframe(df, filter_dict, include=False)
        df = column_cleaner.standardise_column_names(df)
        df[cols.stu_pass].replace({'P': 1}, inplace=True)
        df_data_prev_yr.update({management_type: df})


    # Get the metrics to generate the reports for
    metrics = config['metrics']

    # Get the median aggregate dictionary to calculate median values in report
    median_agg_dict = config['agg_dict_median']

    # Get the standard deviation aggregate dictionary to calculate standard deviation values in report
    std_dev_agg_dict = config['agg_dict_std']
    sub_mark = config['sub_mark']
    sub_group = config['subjects']

    # Loop to generate report for each metric
    for metric in metrics:
        df_dict_metric_wise_sub = get_metric_subj_wise_med_sd_rpt(metric, df_data_curr_yr, df_data_prev_yr,
                                    median_agg_dict, std_dev_agg_dict, sub_mark, sub_group)

        # Save the metric report
        dir_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('data_for_cluster_analysis')
        file_utilities.save_to_excel(df_dict_metric_wise_sub, 'HSC_' + metric + '_subj_wise_rpt_both_years.xlsx', dir_path=dir_path)


if __name__ == "__main__":
    main()



