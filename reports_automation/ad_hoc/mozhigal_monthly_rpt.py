"""
Script to extract mozhigal student access monthly report to create district-wise abstract and district-level abstract
"""
import sys
sys.path.append('../')
import pandas as pd
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import utilities.report_splitter_utilities as report_splitter

def get_se_stu_monthly_rpt(df, group_cols,agg_dict):
    """
    Function to get
    Args:
        df:
        group_cols:

    Returns:

    """
    # Created an empty dictionary to store the District abstract and District level data
    df_rpt_dict = dict()

    # Getting the District Abstract
    df_rpt = df.groupby(by=group_cols).agg(agg_dict).reset_index()
    df_rpt.replace(to_replace={cols.udise_col: cols.tot_schools}, inplace=True)
    df_rpt[cols.total_schls_not_logged_in] = df.groupby(by=group_cols)[cols.logged_in_flag].apply(
        lambda x: (x == 'No').sum()).values
    # Getting Grand Total for the Abstract Report
    # Getting Student Login %
    df_rpt[cols.stu_login_perc] = (df_rpt[cols.total_se_stu_logged_in]/df_rpt[cols.total_se_students])
    df_rpt[cols.stu_login_perc] = df_rpt[cols.stu_login_perc].apply(lambda x: f"{x:.2%}")
    df_rpt.rename(columns= {cols.udise_col: cols.tot_schools}, inplace=True)

    stu_login_perc = (df_rpt[cols.total_se_stu_logged_in].sum() / df_rpt[cols.total_se_students].sum())
    stu_login_perc = f"{stu_login_perc:.2%}"
    rpt_cols = {
        cols.district_name: cols.grnd_total,
        cols.tot_schools: df_rpt[cols.tot_schools].sum(),
        cols.total_se_students: df_rpt[cols.total_se_students].sum(),
        cols.total_se_stu_logged_in: df_rpt[cols.total_se_stu_logged_in].sum(),
        cols.total_schls_not_logged_in: df_rpt[cols.total_schls_not_logged_in].sum(),
        cols.stu_login_perc: stu_login_perc
    }
    # Append the "Grand Total" row with ignore_index=True
    df_rpt = df_rpt.append(rpt_cols, ignore_index=True)

    # Sorting the District names for a better user perspective
    df.sort_values(by=[cols.district_name], inplace=True, ignore_index=True)
    # Splitting the report based on each district
    df_dict = report_splitter.split_report(df, cols.district_name)

    # Finding the percentage for each district
    for dist, df in df_dict.items():
        stu_login_perc = (df[cols.total_se_stu_logged_in].sum() / df[cols.total_se_students].sum())
        stu_login_perc = f"{stu_login_perc:.2%}"
        rpt_cols = {
            cols.block_name: cols.grnd_total,
            cols.udise_col: "",
            cols.school_name: "",
            cols.school_type: "",
            cols.total_schls_not_logged_in:"",
            cols.total_se_students: df[cols.total_se_students].sum(),
            cols.total_se_stu_logged_in: df[cols.total_se_stu_logged_in].sum(),
            cols.stu_logged_in_less_10_min: df[cols.stu_logged_in_less_10_min].sum(),
            cols.stu_logged_in_10_to_30_min: df[cols.stu_logged_in_10_to_30_min].sum(),
            cols.stu_logged_in_more_30_min: df[cols.stu_logged_in_more_30_min].sum(),
            cols.stu_login_perc: stu_login_perc
        }
        print(df[cols.logged_in_flag].value_counts())
        df[cols.logged_in_flag] = df[cols.logged_in_flag].replace({'Yes': 'No', 'No': 'Yes'})
        print(df[cols.logged_in_flag].value_counts())

        df.rename(columns={
            cols.logged_in_flag: cols.total_schls_not_logged_in
        }, inplace=True)
        df[cols.stu_login_perc] = (df[cols.total_se_stu_logged_in] / df[cols.total_se_students])
        df[cols.stu_login_perc] = df[cols.stu_login_perc].apply(lambda x: f"{x:.2%}")
        df = df[list(rpt_cols.keys())]
        #grnd_tot = {cols.grnd_total: [df[cols.total_se_students].sum(axis=1), df[cols.total_se_stu_logged_in].sum(axis=1)]}
        #df.loc[len(df)+1] = rpt_cols
        # Append the "Grand Total" row with ignore_index=True
        df = df.append(rpt_cols, ignore_index=True)
        df_dict.update({dist: df})

    df_rpt_dict.update({"District_Abstract": df_rpt})
    df_rpt_dict.update(df_dict)

    return df_rpt_dict

def main():
    """
    Main function that calls other internal functions to generate the report

    """
    # Ask the user to select the excel file to clean the columns.
    report = file_utilities.user_sel_excel_filename()
    df_report = pd.read_excel(report, sheet_name='MOZHIGAL_STU_LOGIN_DTLS')
    df_report = column_cleaner.standardise_column_names(df_report)
    # Define the levels to group the data by
    grouping_levels = [cols.district_name]
    agg_dict = {
        cols.udise_col: "count",
        cols.total_se_students: "sum",
        cols.total_se_stu_logged_in: "sum"
    }
    df_master_rpt = get_se_stu_weekly_rpt(df_report, grouping_levels, agg_dict)
    dir_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('Mozhigal')
    file_utilities.save_to_excel(df_master_rpt,  'mozhigal.xlsx', dir_path=dir_path)


if __name__ == "__main__":
    main()