
"""
Module to create analysis report for people teacher ratio of SSLC.
"""

import sys

import pandas as pd

sys.path.append('../')

import utilities.column_names_utilities as cols
import readers.config_reader as config_reader
import readers.data_fetcher as data_fetcher
import utilities.utilities as utilities
import utilities.file_utilities as file_utilities


def main():
    """

    Script to create the report for people teacher ratio for SSLC all management Current year data
    -------

    """

    # Fetch the configuration for creating the reports
    config = config_reader.get_config('12TH_SUBJECTS_GROUPING', 'miscellaneous_configs')
    config = cols.update_nested_dictionaries(config)

    # Get the current year data set for all management types
    source_config_curr_yr = config['source_config_curr_yr']
    sources_curr_yr = data_fetcher.get_data_set_from_config(source_config_curr_yr, "miscellaneous_configs")

    # Data cleaning - excluding invalid values from the dataframe
    filter_dict = config['filter_dict']

    for key in sources_curr_yr.keys():
        sources_curr_yr[key] = utilities.filter_dataframe(sources_curr_yr[key], filter_dict, include=False)

    # get the grouping level
    grouping_lvl = [cols.district_name, cols.block_name, cols.management, cols.udise_col, cols.school_name]

    # get the agg dict for class 12
    agg_dict = {
        cols.tot_stu: "count",
        cols.stu_pass: "sum",
        cols.tot_marks: "median",
        cols.lang_marks: "median",
        cols.eng_marks: "median",
        cols.math_marks: "median",
        cols.physics: "median",
        cols.chemistry: "median",
        cols.biology: "median",
        cols.economics: "median",
        cols.commerce: "median",
        cols.computer_science: "median"
    }

    # get the agg dict for class 12
    #agg_dict = {
        #cols.tot_stu: "count",
        #cols.stu_pass: "sum",
        #cols.tot_marks: "median",
        #cols.lang_marks: "median",
        #cols.eng_marks: "median",
        #cols.math_marks: "median",
        #cols.science_marks: "median",
        #cols.social_marks: "median"}

    # Create an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    for key, df in sources_curr_yr.items():
        #print('df columns before concat', df.columns.to_list())
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Convert total mark column to integer
    combined_df[cols.tot_marks] = combined_df[cols.tot_marks].fillna(0).astype('int')
    #combined_df[cols.tot_marks] = combined_df[cols.tot_marks].astype('int')
    #ombined_df[cols.lang_marks] = combined_df[cols.lang_marks].astype('int')
    #combined_df[cols.eng_marks] = combined_df[cols.eng_marks].astype('int')
    #combined_df[cols.math_marks] = combined_df[cols.math_marks].astype('int')
    #combined_df[cols.science_marks] = combined_df[cols.science_marks].astype('int')
    #combined_df[cols.social_marks] = combined_df[cols.social_marks].astype('int')

    # Combine DataFrames with Grouping Levels
    combined_df_grouped = combined_df.groupby(grouping_lvl).agg(agg_dict)

    # Get the class 10 PTR data
    cls_10_ptr = pd.read_excel(r'C:\Users\Admin\Desktop\data analysis\PTR/class 12 ptr.xlsx', sheet_name='Details')

    # Merge the two DataFrames based on a common column.
    sslc_ptr = pd.merge(combined_df_grouped, cls_10_ptr, how='inner', on=[cols.udise_col])

    #Add pass % in a new column hsc
    sslc_ptr[cols.stu_pass] = pd.to_numeric(sslc_ptr[cols.stu_pass], errors='coerce')
    sslc_ptr[cols.tot_stu] = pd.to_numeric(sslc_ptr[cols.tot_stu], errors='coerce')

    pass_perc = sslc_ptr[cols.stu_pass] / sslc_ptr[cols.tot_stu]
    sslc_ptr[cols.pass_perc] = round(pass_perc, 2)

    # Save the metric report
    dir_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('PTR')
    file_utilities.save_to_excel({'sslc_ptr': sslc_ptr}, 'HSC_ptr_rpt.xlsx', dir_path=dir_path)

if __name__ == '__main__':
    main()
