import datetime
import pymssql, pyodbc
import pandas as pd
import io
import traceback

from pdia.utils.logger import logger
import warnings


# # SQL Query functions

# password = getpass.getpass(prompt='Enter your password: ')

def sql2df(sql, password,
            server="1.2.3.4:5678",
            user="XXX\\XXXX",
            database="DATABASE_NAME",
            verbose=True,
            method="pymssql", trustedConnection=False):
    """
    Query a SQL Server with a SQL query, and returns the returned data as a pandas data frame. Note that you should
    not use this to transfer large amount of data, as the pandas df is memory-limited.

    :param sql: the SQL query string
    :param password: the password for SQl authentication
    :param server: the IP address of the SQl server, with port number.
    :param user: the SQL server logon
    :param database: a string of the SQL data base name
    :param verbose: print date time, etc.; default to True
    :param method: SQL library to use; default to "pymssql", can also be "pyodbc"
    :param trustedConnection: use Windows login if True; default to False.
    :return: a pandas data frame, or None
    """

    # Connect to MSSQL Server
    if verbose:
        print(str(datetime.datetime.now()))
        print("sql2csv(): Connecting to the SQL server {}".format(server))

    conn = None
    if method == "pymssql":
        try:
            conn = pymssql.connect(server=server,
                               user=user,
                               password=password,
                               database=database)
        except Exception as e:
            warnings.warn("sql2df failed: no connection")
            logger.error("sql2df:")
            logger.exception(e)
            exc_buffer = io.StringIO()
            traceback.print_exc(file=exc_buffer)
            logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
    elif method == "pyodbc":
        connectString = ""
        if trustedConnection:
            connectString = \
                "DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={};DATABASE={};Trusted_Connection=yes;" \
                    .format(server, database)
        else:
            connectString = \
                "DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={};DATABASE={};UID={};PWD={};" \
                    .format(server, database, user, password)
        try:
            conn = pyodbc.connect(connectString)
        except Exception as e:
            warnings.warn("sql2df failed: no connection")
            logger.error("sql2df:")
            logger.exception(e)
            exc_buffer = io.StringIO()
            traceback.print_exc(file=exc_buffer)
            logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
            conn = None

    if conn is None:
        if verbose:
            print(str(datetime.datetime.now()))
            print("sql2csv(): Connection failed to {}".format(server))
        return

    # get ready to read
    df = None
    try:
        df = pd.read_sql(sql, conn)
    except Exception as e:
        warnings.warn("sql2df failed to return valid data")
        logger.error("sql2df:")
        logger.exception(e)
        exc_buffer = io.StringIO()
        traceback.print_exc(file=exc_buffer)
        logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
        return None

    if verbose:
        print(str(datetime.datetime.now()))
        print("sql2df(): Disconnecting from the SQL server {}".format(server))
    # Close the database connection
    conn.close()

    return df
