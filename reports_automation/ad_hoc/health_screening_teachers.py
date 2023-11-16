import sys

sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.format_utilities as format_utilities
import utilities.dbutilities as dbutilities
import utilities.column_names_utilities as cols
import data_cleaning.column_cleaner as column_cleaner
import pandas as pd

# Read the excel report as a Pandas DataFrame object
df_report_pmoa = pd.read_excel(r'C:\Users\TAMILL\Downloads\PMOA-Screening-rpt.xlsx',sheet_name='Report', skiprows=4)
df_report_mht = pd.read_excel(r'C:\Users\TAMILL\Downloads/mht_scr_rpt.xlsx',sheet_name='Report', skiprows=4)
df_report_spectacle = pd.read_excel(r'C:\Users\TAMILL\Downloads\Spect-Manage-rpt.xlsx',sheet_name='Block-Wise Report', skiprows=4)


def get_pmoa_screening_status(df, group_level):
    """
    Function to get the PMOA screening status of students at a given grouping level (district/educational district/block)

    Parameters:
    ----------
    df: Pandas DataFrame object
        The data from which summary of grouped level wise screening status of students is to be extracted
    group_level: str
        The column name in the data to group by (Eg: district/educational district/block)
    Returns:
    --------
    The grouped level wise screening status of students as a Pandas DataFrame object
    """

    # Group the data down to given grouping level,
    # counting total students, students screened, not screened, referred to MHT and referred to PMOA

    df_group_level = df.groupby([group_level], sort=False)[
        ['Total', 'Teacher_Screened', 'Referred to PMOA', 'Referred_Screened', 'Added_students', 'PMOA_Screened',
         'Spectacle Needed',
         'Visit to DEIC', 'Spectacle Needed and Visit to DEIC', 'Screening completed (No action)']].sum().reset_index()

    # Add a % students screened column to the dataframe
    # Insert the column to the right of Screened column
    pmoa_screened_col_index = df_group_level.columns.get_loc('Screening completed (No action)')
    df_group_level.insert(pmoa_screened_col_index + 1, '% PMOA_Screened',
                          df_group_level['Referred_Screened'] / df_group_level['Referred to PMOA'])

    df_group_level.insert(pmoa_screened_col_index + 2, 'Spectacles needed',
                          df_group_level['Spectacle Needed'] + df_group_level['Spectacle Needed and Visit to DEIC'])
    df_group_level.insert(pmoa_screened_col_index + 3, '% Spectacles necessary',
                          df_group_level['Spectacle Needed'] / df_group_level['PMOA_Screened'])
    df_group_level.insert(pmoa_screened_col_index + 4, 'DEIC referral',
                          (df_group_level['Visit to DEIC'] + df_group_level['Spectacle Needed and Visit to DEIC']) /
                          df_group_level['PMOA_Screened'])
    # sorting the data
    df_group_level = df_group_level.sort_values(['% PMOA_Screened'], ascending=[True])

    # Calculate grand total
    df_group_level.loc['Grand Total'] = [
        'Grand Total',
        df_group_level['Total'].sum(),
        df_group_level['Teacher_Screened'].sum(),
        df_group_level['Referred to PMOA'].sum(),
        df_group_level['Referred_Screened'].sum(),
        df_group_level['Added_students'].sum(),
        df_group_level['PMOA_Screened'].sum(),
        df_group_level['Spectacle Needed'].sum(),
        df_group_level['Visit to DEIC'].sum(),
        df_group_level['Spectacle Needed and Visit to DEIC'].sum(),
        df_group_level['Screening completed (No action)'].sum(),
        df_group_level['% PMOA_Screened'].mean(),
        df_group_level['Spectacles needed'].sum(),
        df_group_level['% Spectacles necessary'].mean(),
        df_group_level['DEIC referral'].mean()]

    # percentage formatting
    df_group_level.loc[:, '% PMOA_Screened'] = df_group_level['% PMOA_Screened'].map('{:.0%}'.format)
    df_group_level.loc[:, '% Spectacles necessary'] = df_group_level['% Spectacles necessary'].map('{:.0%}'.format)
    df_group_level.loc[:, 'DEIC referral'] = df_group_level['DEIC referral'].map('{:.0%}'.format)

    return df_group_level


def get_mht_screening_status(df, group_level):
    """
    Function to get the MHT screening status of students at a given grouping level (district/educational district/block)

    Parameters:
    ----------
    df: Pandas DataFrame object
        The data from which summary of grouped level wise screening status of students is to be extracted
    group_level: str
        The column name in the data to group by (Eg: district/educational district/block)
    Returns:
    --------
    The grouped level wise screening status of students as a Pandas DataFrame object
    """

    df_group_level = df.groupby([group_level], sort=False)[
        ['Total', 'Teacher_Screened', 'Referred to MHT', 'Referred_Screened', 'Added_students', 'MHT_Screened',
         'Referred to DEIC',
         'Referred to PHC / CHC / Sub-district hospital', 'Treatment given during camp']].sum().reset_index()

    # Add a % students screened column to the dataframe
    # Insert the column to the right of Screened column
    mht_screened_col_index = df_group_level.columns.get_loc('Treatment given during camp')
    df_group_level.insert(mht_screened_col_index + 1, '% MHT Screened',
                          df_group_level['Referred_Screened'] / df_group_level['Referred to MHT'])

    df_group_level.insert(mht_screened_col_index + 2, '% DEIC referral',
                          df_group_level['Referred to DEIC'] / df_group_level['MHT_Screened'])

    # sorting the data
    df_group_level = df_group_level.sort_values(['% MHT Screened'], ascending=[True])

    # Calculate grand total
    df_group_level.loc['Grand Total'] = [
        'Grand Total',
        df_group_level['Total'].sum(),
        df_group_level['Teacher_Screened'].sum(),
        df_group_level['Referred to MHT'].sum(),
        df_group_level['Referred_Screened'].sum(),
        df_group_level['Added_students'].sum(),
        df_group_level['MHT_Screened'].sum(),
        df_group_level['Referred to DEIC'].sum(),
        df_group_level['Referred to PHC / CHC / Sub-district hospital'].sum(),
        df_group_level['Treatment given during camp'].sum(),
        df_group_level['% MHT Screened'].mean(),
        df_group_level['% DEIC referral'].mean()]

    # percentage formatting
    df_group_level.loc[:, '% MHT Screened'] = df_group_level['% MHT Screened'].map('{:.0%}'.format)
    df_group_level.loc[:, '% DEIC referral'] = df_group_level['% DEIC referral'].map('{:.0%}'.format)
    return df_group_level


def get_spectacle_Status(df, group_level):
    """
    Function to get the PMOA screening status of students at a given grouping level (district/educational district/block)

    Parameters:
    ----------
    df: Pandas DataFrame object
        The data from which summary of grouped level wise spectacle  screening status of students is to be extracted
    group_level: str
        The column name in the data to group by (Eg: district/educational district/block)
    Returns:
    --------
    The grouped level wise screening status of students as a Pandas DataFrame object
    """
    df_group_level = df.groupby([group_level], sort=False)[
        ['Total Students with refractive error', 'PMOA Screened, PO not sent by HUD', 'Purchase Order Upload Pending',
         'Total Orders sent by HUD',
         'Not accepted by Vendor', 'Accepted by Vendor']].sum().reset_index()

    # Add a % students screened column to the dataframe
    # Insert the column to the right of Screened column
    Spectacle_Status_col_index = df_group_level.columns.get_loc('Accepted by Vendor')
    df_group_level.insert(Spectacle_Status_col_index + 1, '% Sent by HUD',
                          df_group_level['Total Orders sent by HUD'] / df_group_level['Total Students with refractive error'])

    df_group_level.insert(Spectacle_Status_col_index + 2, '% Accepted by Vendor',
                          df_group_level['Accepted by Vendor'] / df_group_level['Total Orders sent by HUD'])

    # sorting the data
    df_group_level = df_group_level.sort_values(['% Sent by HUD'], ascending=[True])
    # Calculate grand total
    df_group_level.loc['Grand Total'] = [
        'Grand Total',
        df_group_level['Total Students with refractive error'].sum(),
        df_group_level['PMOA Screened, PO not sent by HUD'].sum(),
        df_group_level['Purchase Order Upload Pending'].sum(),
        df_group_level['Total Orders sent by HUD'].sum(),
        df_group_level['Not accepted by Vendor'].sum(),
        df_group_level['Accepted by Vendor'].sum(),
        df_group_level['% Sent by HUD'].mean(),
        df_group_level['% Accepted by Vendor'].mean()]

    # percentage formatting
    df_group_level.loc[:, '% Sent by HUD'] = df_group_level['% Sent by HUD'].map('{:.0%}'.format)
    df_group_level.loc[:, '% Accepted by Vendor'] = df_group_level['% Accepted by Vendor'].map('{:.0%}'.format)

    # Calculate grand total
    return df_group_level


def main():
    # Get the schools' health screening details at district level
    # path to save the file
    directory_path = file_utilities.get_curr_day_month_gen_report_name_dir_path('health_screening')

    df_schools_screening_status_pmoa = get_pmoa_screening_status(df_report_pmoa, cols.district_name)
    file_utilities.save_to_excel({'Report': df_schools_screening_status_pmoa}, 'pmoa.xlsx', dir_path=directory_path)

    df_schools_screening_status_mht = get_mht_screening_status(df_report_mht, cols.district_name)
    file_utilities.save_to_excel({'Report': df_schools_screening_status_mht}, 'mht.xlsx', dir_path=directory_path)

    df_schools_screening_status_spectacle = get_spectacle_Status(df_report_spectacle, cols.district_name)
    file_utilities.save_to_excel({'Report': df_schools_screening_status_spectacle}, 'spectacle.xlsx', dir_path=directory_path)



if __name__ == "__main__":
    main()
