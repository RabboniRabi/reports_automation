import sys

sys.path.append('../')
import pandas as pd
import utilities.file_utilities as file_utilities

def data_prep(stud_det_df:pd.DataFrame,metric_type:list):
    """
    Function to merge the student mark details dataframe with the list of different type of metrics.

    Parameters:
        stud_det_df:pd.DataFrame
           Data frame with student details with their marks

        metric_type: list
           The list of dataframe with different metrics to be merged.

    Returns:
           The merged dataframe with student details and the given metric.
    """

    for df in metric_type:
        stud_det_df = pd.merge(stud_det_df,df,how= 'left',on ='EMIS_NO')
    return stud_det_df

def main():
    # The dataframe with student mark details for defined management type
    aided = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\SSLC_stud_level_government_2022-23.xlsx')
    print("Data successfully read")

    # The dataframe with mother's qualification details
    moth_qual = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_moth_qual.xlsx')
    print("Data successfully read")

    # The dataframe with mother's occupation details
    moth_occ = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_moth_occ.xlsx')
    print("Data successfully read")

    # The dataframe with father's qualification details
    fath_qual = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_fath_qual.xlsx')
    print("Data successfully read")

    # The dataframe with father's occupation details
    fath_occ = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_fath_occ.xlsx')
    print("Data successfully read")

    # The dataframe with parent's income details
    parent_inc = pd.read_excel(r'C:\Users\TAMILL\Data Reporting\reports\source_data\Oct_23\sslc\sslc_parent_income.xlsx')
    print("Data successfully read")

    # list with different metrics to be merged
    metric_list = [moth_qual,moth_occ,fath_qual,fath_occ,parent_inc]
    df_prep = data_prep(aided,metric_list)

    # To save as excel file
    directory_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('data_preperation_10')
    file_utilities.save_to_excel({'Report': df_prep},'govt.xlsx', dir_path=directory_path)



if __name__ == "__main__":
    main()
