import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

import json

def read_credentials(file_path):
    """
    Function to read the credentials stored in a given file (with full path)
    in dictionary or JSON format
    Parameters:
    ----------
    file_path: str
        The full path to the file
    Returns:
    -------
    The dictionary supplied in the file
        {
            "username": "<username>",
            "password": "<password>",
            "db_name": "<dbname>",
            "host_name": "<hostname>"
        }
    """
    file = open(file_path, mode = 'r')
    data = file.read()
    credentials_dict = json.loads(data)
    file.close()
    print ('credentials_dict: ', credentials_dict)
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

