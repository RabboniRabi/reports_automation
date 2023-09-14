import sys
sys.path.append('../')

import utilities.file_utilities as file_utilities
import utilities.utilities as utilities


def main():
    """
    Main function to read the master OoSC survey target data
    and update with the latest report.

    """
    # Get the path to the master Oosc survey target file
    gen_reports_dir_path = file_utilities.get_gen_reports_dir_path()
    master_file_path = file_utilities.get_file_path('OOSC_Survey_2023_24_Target_Report.xlsx', gen_reports_dir_path)
    df_master_data = file_utilities.read_sheet(master_file_path, sheet_name='Details')

    # Get the path to the latest OoSC survey target file
    new_file_path = file_utilities.get_file_path('OOSC_Sur_23_24_Tar_Rpt.xlsx',
                                                 file_utilities.get_curr_month_source_data_dir_path())
    df_new_data = file_utilities.read_sheet(new_file_path, sheet_name='Details')

    # Update the master data with the latest file, adding only new entries
    df_oosc_survey_report = utilities.update_master_data(df_master_data, df_new_data)

    print(df_oosc_survey_report)
    # Replace the existing master data with the new updated master data
    file_utilities.save_to_excel({'Details': df_oosc_survey_report},
                                 'OOSC_Survey_2023_24_Target_Report.xlsx',
                                 dir_path=gen_reports_dir_path)


if __name__ == "__main__":
    main()
