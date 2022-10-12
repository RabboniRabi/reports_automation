
import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.dbutilities as dbutilities
import pandas as pd
import os


columns = [
    'District', 'Student Name', 'guardian_name', 'Student Reference ID', 'Mobile', 
'Batch', 'Current School', 'Class 6 School', 'Class 7 School', 'Class 8 School',
'Class 9 School', 'Class 10 School', 'Class 11 School', 'Class 12 School', 'C6_District', 
'C7_District', 'C8_District', 'C9_District', 'C10_District', 'C11_District', 'C12_District',
'Class VI Status', 'Class VII Status','Class VIII Status', 'Class IX Status', 'Class X Status',
'Class XI Status', 'Class XII Status', 'C6_Type', 'C7_Type', 'C8_Type', 'C9_Type', 
'C10_Type', 'C11_Type', 'C12_Type', 'Verified_status'
]



def get_data_as_df(credentials_dict):
    """
    Function to query the database and return the mra status data as a pandas datafram object
    
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

    Returns
    -------
    MRA status data as a dataframe object
    """

    connection = dbutilities.create_server_connection(credentials_dict)

    query = utilities.open_scripts().read()

    df_data = pd.read_sql_query(query, connection) 

    # Close the database connection
    connection.close()

    return df_data

def label_status(df, start_column, end_column):
    """
    Function to label status of verification for each entry as Rejected, Approved, Pending.
    The function also creates three corresponding columns: Rejected, Approved & Pending.
    If the status of a particular entry is Approved, 1 in entered in the cell and 0 in the 
    other two cells. Similarly for other statuses.
    The numeric values in these three columns will help in grouping & pivoting

    Parameters:
    ----------
    df: Pandas DataFrame
        The data frame to work on
    start_column: str
        The start of the column range
    end_column: str
        The end of the column range        
    """
    df_subset = df.loc[:, start_column:end_column]
    
    no_of_columns = df_subset.shape[1]

    for row in (range(0, df_subset.shape[0])):
        df_row = df_subset.iloc[row]
        rejected_count = df_row[df_row == 'Rejected'].count()
        verified = df.iloc[row, df.columns.get_loc('Verified_status')] == 'Verified'
        approved_count = df_row[df_row == 'Approved'].count()
        if (rejected_count > 0 and verified):
            df.at[row,'Status'] = 'Rejected'
            df.at[row,'Rejected'] = 1
            df.at[row,'Approved'] = 0
            df.at[row,'Pending'] = 0
        elif (approved_count == no_of_columns and verified): # All columns are approved
            df.at[row,'Status'] = 'Approved'
            df.at[row,'Rejected'] = 0
            df.at[row,'Approved'] = 1
            df.at[row,'Pending'] = 0
        else:
            df.at[row,'Status'] = 'Pending'    
            df.at[row,'Rejected'] = 0
            df.at[row,'Approved'] = 0
            df.at[row,'Pending'] = 1

def group_and_count_statuses(df, group_by):
    """
    Function to group the data by given group_by column name

    Parameters:
    ----------
    df: pandas dataframe object
        The data to group and count statuses
    group_by:
        The attribute to group by

    Returns:
    -------
    Grouped data frame object    
    """
    # Group & count statuses
    df_data_grouped = df.groupby(group_by)[['Approved', 'Rejected', 'Pending']].sum()

    # Count the total verified statuses for each row
    df_data_grouped['Verified'] = df_data_grouped['Approved'] + df_data_grouped['Rejected']

    # Count the total number of all statuses for each row
    df_data_grouped['Total'] = df_data_grouped['Verified'] + df_data_grouped['Pending']

    df_data_grouped['% Verified'] = df_data_grouped['Verified']/df_data_grouped['Total']

    # Sort by % Verified
    df_data_grouped.sort_values(by=['% Verified'], ascending=False, inplace=True)

    # Convert values to percentage and upto two decimal places
    df_data_grouped.loc[:, '% Verified'] = df_data_grouped['% Verified'].astype(float).map('{:.2%}'.format)

    return df_data_grouped



def main():

    # Read the credentials and get a database connection
    curr_dir = os.getcwd()
    output_data_path = '../credentials/'
    file_path = os.path.join(curr_dir, output_data_path, 'db_credentials.json')
    
    credentials_dict = dbutilities.read_credentials(file_path)

    # Query and get the data
    df_data = get_data_as_df(credentials_dict)

    # Label the statuses
    label_status(df_data,'Class VI Status', 'Class XII Status')

    # Group the statuses district wise
    df_data_grouped = group_and_count_statuses(df_data, 'District')   

    # Remove the columns 'Approved', 'Rejected', 'Pending' that were used for grouping
    df_data.drop(columns=df_data.columns[-3:],axis=1, inplace=True)                     

    # Save data
    df_sheet_dict = {'Data':df_data, 'Status report':df_data_grouped}
    file_name = utilities.get_date_appended_excel_filename('MRA_Status')
    utilities.save_to_excel(df_sheet_dict, file_name, index=True)

if __name__ == "__main__":
    main()


