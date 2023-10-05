import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

import json
import os
import sys

import utilities.file_utilities as file_utilities
import pandas as pd
import pandas.io.sql as psql
from pandas.io.sql import DatabaseError


def read_conn_credentials(file_name):
    """
    Function to read the connection and credential details stored 
    in dictionary or JSON format in file with given name 
    Parameters:
    ----------
    file_name: str
        The name of file with credentials and connection details to connect to a database
    Returns:
    -------
    A dictionary with connection details and credentials read from the file
        {
            "username": "<username>",
            "password": "<password>",
            "db_name": "<dbname>",
            "host_name": "<hostname>"
        }
    """
    curr_dir = os.getcwd()
    cred_dir_path = '../credentials/'
    file_path = os.path.join(curr_dir, cred_dir_path, file_name)
    file = open(file_path, mode='r')
    data = file.read()
    credentials_dict = json.loads(data)
    file.close()
    return credentials_dict


def create_server_connection(credentials_dict):
    """
    Function to create a database server connection given host name, username and password
    
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
    ------
    A database connection object if connection is successful. Error otherwise.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=credentials_dict['host_name'],
            user=credentials_dict['username'],
            passwd=credentials_dict['password'],
            database=credentials_dict['db_name']
        )
        print('Database connection successful')
    except Error as err:
        print(f'Error: ', err)
    return connection


def get_sqlalchemy_conn_obj(host, port, db_name, user_name, password):
    """
    """
    try:
        dialect_driver = 'mysql://' + user_name + ':' + password + '@' \
                         + host + ':' + port + '/' + db_name
        print('dialect driver: ', dialect_driver)
        connection = create_engine(dialect_driver).connect()
        print('Database connection successful')
    except Error as err:
        print('Error: ', err)
    return connection


def fetch_data(connection, query):
    """
    Function to fetch data by executing a read query

    Parameters
    ----------
    connection: mysql.connector.connection_cext.CMySQLConnection
        connection object
    query: str 
    The fetch query to be executed

    Returns
    -------
    Results of fetch query
    """

    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f'Error: ', err)


def fetch_data_as_df(credentials_dict, script_file_name, params:list=None):
    """
    Function to fetch data from the database using a query and return the data as a pandas dataframe object

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
    params: list
        Optional list of parameters for query (Default is None)
    Returns
    -------
    Query results as a dataframe object
    """
    connection = create_server_connection(credentials_dict)
    query = file_utilities.open_script(script_file_name).read()
    try:
        print('Executing Query...')
        # If parameters for the query are given, update the query
        if params is not None:
            query = query.format(*params)
        df_data = pd.read_sql_query(query, connection)
        print('Query Execution Successful')
    except (DatabaseError, Error) as err:
        print(f'Error: ', err)
        err_msg = 'Error in executing query in ' + script_file_name
        sys.exit(err_msg)

    # Close the database connection
    connection.close()

    return df_data


def fetch_data_in_batches_as_df(credentials_dict, script_file_name, batch_size=100000, params=None):
    """
    Function to fetch data in batches from the database using a query and return the data as a pandas dataframe object
    
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
    batch_size: int
        The number of rows to fetch in each batch query
    script_file_name: str
        The file name with the sql script to be executed to fetch the data
    Returns
    -------
    Query results as a dataframe object
    """
    connection = create_server_connection(credentials_dict)
    query = file_utilities.open_script(script_file_name).read()

    offset = 0
    dfs = []

    print('Executing Query...')
    try:
        while True:
            print('Batch Query from offset: ', offset)

            # Update the query to include the size of result to fetch and the offset index
            batch_query = query % (batch_size, offset)
            dfs.append(pd.read_sql_query(batch_query, connection))

            # Change the offset for the next batch
            offset += batch_size
            # If number of rows fetched in last batch query is less than batch size,
            # no more rows to fetch
            if len(dfs[-1]) < batch_size:
                break
        full_df = pd.concat(dfs)
        print('Query Execution Successful')
    except (DatabaseError, Error) as err:
        print(f'Error: ', err)
        err_msg = 'Error in executing query in ' + script_file_name
        sys.exit(err_msg)

    # Close the database connection
    connection.close()

    return full_df


