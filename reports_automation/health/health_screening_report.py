import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import pandas as pd

# Global variables
district = 'District'


# Read the excel report as a Pandas DataFrame object
#df_report = pd.read_excel(r'/home/rabboni/Downloads/Student-health-checkup-rpt.xlsx', sheet_name='Report',skiprows=4)

def get_students_screening_status(df, group_level):
    """
    Function to get the screening status of students at a given grouping level (district/educational district/block)

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
    df_group_level = df.groupby([group_level],sort=False)[
    ['Total', 'Screened', 'UnScreened', 'Referred to MHT', 'Referred to PMOA']].sum().reset_index()

    # Add a % students screened column to the dataframe
    # Insert the column to the right of Screened column
    screened_col_index = df_group_level.columns.get_loc('Screened')        
    df_group_level.insert(screened_col_index+1,'% Screened', df_group_level['Screened']/df_group_level['Total'])
    df_group_level.loc[:, '% Screened'] = df_group_level['% Screened'].map('{:.2%}'.format)

    # Add a % Referred to MHT column to the dataframe
    # Insert the column to the right of Referred to MHT column
    mht_col_index = df_group_level.columns.get_loc('Referred to MHT')
    df_group_level.insert(mht_col_index+1,'% Referred to MHT', df_group_level['Referred to MHT']/df_group_level['Screened'])
    df_group_level.loc[:, '% Referred to MHT'] = df_group_level['% Referred to MHT'].map('{:.2%}'.format)   

    # Add a % Referred to PMOA column to the dataframe
    # Insert the column to the right of Referred to PMOA column
    pmoa_col_index = df_group_level.columns.get_loc('Referred to PMOA')
    df_group_level.insert(pmoa_col_index+1,'% Referred to PMOA', df_group_level['Referred to PMOA']/df_group_level['Screened'])
    df_group_level.loc[:, '% Referred to PMOA'] = df_group_level['% Referred to PMOA'].map('{:.2%}'.format)

    # Sort the data by % Screened
    df_group_level = df_group_level.sort_values(['% Screened'], ascending=[False])

    df_group_level.rename(columns = {'Total':'Total Students'}, inplace = True)

    df_group_level.drop(columns=['UnScreened'], inplace = True)

    # Trying colour gradients

    
    #df_group_level.style.background_gradient(axis=0,subset=['% Screened'], cmap='Blues').to_excel('please_work.xlsx', engine='openpyxl')

    return df_group_level

def get_schools_screening_status(df, group_level):
    """
    Function to get the screening status of schools at a given grouping level (district/educational district/block)
    
    Parameters:
    ----------
    df: Pandas DataFrame object
        The data from which summary of grouped level wise screening status of schools is to be extracted
    group_level: str
        The column name in the data to group by (Eg: district/educational district/block)
    Returns:
    --------
    The grouped level wise screening status of schools as a Pandas DataFrame object 
    """

    # Compute whether a school has completed screening, partially completed or not started
    series_completed = (df['Total'] - df['Screened'] == 0 ) & (df['Total']  != 0) 
    series_not_started =  df['Screened'] == 0
    series_partially_completed =  ~(series_completed | series_not_started)
    school_col_index = df.columns.get_loc('School')            
    # Insert the computed values as series into the dataframe next to the school column
    df.insert(school_col_index+1,'Fully completed', series_completed)
    df.insert(school_col_index+2,'Partially Completed', series_partially_completed)
    df.insert(school_col_index+3,'Not started', series_not_started)

    # Group the data down to given grouping level,
    # counting total schools, completed schools, partially completed school, not started schools
    df_group_level = df.groupby([group_level],sort=False).agg(
        Total_Schools=('School', 'count'),
        Fully_Completed_Schools = ('Fully completed', 'sum'),
        Partially_Completed_Schools = ('Partially Completed', 'sum'),
        Not_Started_Schools = ('Not started', 'sum')
    ).reset_index()

    # Rename columns
    df_group_level.rename(columns = {
        'Total_Schools':'Total Schools',
        'Fully_Completed_Schools': 'Fully Completed Schools',
        'Partially_Completed_Schools': 'Partially Completed Schools',
        'Not_Started_Schools': 'Not Started Schools'
        }, inplace = True)

    # Add a column indicated % completed schools at each grouped value
    df_group_level.insert(df_group_level.shape[1], '% Fully completed', df_group_level['Fully Completed Schools']/df_group_level['Total Schools'])

     # Sort the data by % Fully completed
    df_group_level = df_group_level.sort_values(['% Fully completed'], ascending=[False])

    # checking color gradient
    """df_group_level.style\
    .background_gradient(axis=0,subset=['% Fully completed'], cmap='jet')\
    .format({'% Fully completed': '{:.2%}'})\
    .to_excel('please_work.xlsx', engine='openpyxl')"""

    df_group_level.loc[:, '% Fully completed'] = df_group_level['% Fully completed'].map('{:.2%}'.format)   

    return df_group_level





def fetch_data_as_df (credentials_dict, script_file_name):
    """
    Function to query the database for students' health screening details and return the data as a pandas dataframe object
    
    Parameters
    ---------
    credentials_dict: dict
        A dictionary of credentials to use to connect to the database
        eg: {
        "username": "<username>",
        "password": "<password>",
        "db_name": "<dbname>",
        "host_name": "<hostname>"
        }
    script_file_name: str
        The file name with the sql script to be executed to fetch the data
    Returns
    -------
    Students' health screening details as a dataframe object
    """
    connection = dbutilities.create_server_connection(credentials_dict)
    query = file_utilities.open_script(script_file_name).read()

    print('Executing Query...')
    df_data = pd.read_sql_query(query, connection) 
    print('Query Execution Successful')

    # Close the database connection
    connection.close()

    return df_data

def main():
    
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    df = fetch_data_as_df(credentials_dict, 'health_screening_status.sql')

    # Temporarily reading from excel
    #df_report = pd.read_excel(r'/home/rabboni/Downloads/health.xlsx', sheet_name='Report')

    #df_copy = df_report.copy(deep=True)

    # Get the students' health screening details at district level
    df_students_screening_status = get_students_screening_status(df_report, district)


    # Get the schools' health screening details at district level
    df_schools_screening_status = get_schools_screening_status(df_report, district)

    df_sheet_dict = {
    'Students screening status': df_students_screening_status,
    'Schools screening status': df_schools_screening_status
    }

    file_utilities.save_to_excel(df_sheet_dict, 'health_screening_status.xlsx')

      

if __name__ == "__main__":
    main()
