import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

import json
import os

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
    file = open(file_path, mode = 'r')
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
            host = credentials_dict['host_name'],
            user = credentials_dict['username'],
            passwd = credentials_dict['password'],
            database = credentials_dict['db_name']
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

