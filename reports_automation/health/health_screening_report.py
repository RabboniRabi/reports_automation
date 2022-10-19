import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.dbutilities as dbutilities
import pandas as pd

# Global variables
district = 'District'


# Read the excel report as a Pandas DataFrame object
df_report = pd.read_excel(r'/home/rabboni/Downloads/Student-health-checkup-rpt.xlsx', sheet_name='Report',skiprows=4)

def get_students_screening_status(df, group_level):
        """
        Function to get the screening status of students at a given grouping level (district/educational district/block)
        
        Parameters:
        ----------
        df: Pandas DataFrame object
            The original DataFrame object on which subtotaling operations are to be performed
            and subtotal rows to be inserted
        group_level: str
            The column name in the data to group by (Eg: district/educational district/block) 
        """

        # Group the data down to given grouping level level,
        # counting total students, students screened, not screened, referred to MHT and referred to PMOA
        df_group_level = df.groupby([group_level],sort=False)[
        ['Total', 'Screened', 'UnScreened', 'Referred to MHT', 'Referred to PMOA']].sum().reset_index()

        # Add a % students screened column to the dataframe
        df_group_level['% Screened'] = df_group_level['Screened']/df_group_level['Total']
        df_group_level.loc[:, '% Screened'] = df_group_level['% Screened'].map('{:.2%}'.format)

        # Add a % Referred to MHT column to the dataframe
        df_group_level['% Referred to MHT'] = df_group_level['Referred to MHT']/df_group_level['Screened']
        df_group_level.loc[:, '% Referred to MHT'] = df_group_level['% Referred to MHT'].map('{:.2%}'.format)   

        # Add a % Referred to PMOA column to the dataframe
        df_group_level['% Referred to PMOA'] = df_group_level['Referred to PMOA']/df_group_level['Screened']
        df_group_level.loc[:, '% Referred to PMOA'] = df_group_level['% Referred to PMOA'].map('{:.2%}'.format)

        # Sort the data by % Screened
        df_group_level = df_group_level.sort_values(['% Screened'], ascending=[True])

        # print the data to test
        print(df_group_level)

def get_schools_screening_status():
    print ('hello')        


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

    df_data = pd.read_sql_query(query, connection) 

    # Close the database connection
    connection.close()

    return df_data

def main():
    
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the students' health screening details from the database as a Pandas DataFrame object
    df = fetch_data_as_df(credentials_dict, 'health_screening_status.sql')

    # Get the students' health screening details at district level
    get_students_screening_status(df, district)

      

if __name__ == "__main__":
    main()
