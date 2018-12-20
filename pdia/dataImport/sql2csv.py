import csv
import datetime
import pymssql
import pyodbc
import io
import traceback
from pdia.utils.logger import logger


# # SQL Query functions

# password = getpass.getpass(prompt='Enter your password: ')

def sql2csv(sql, csvFileName, password,
            server="1.2.3.4:5678",
            user="XXX\\XXXX",
            database="DATABASE_NAME",
            verbose=True,
            method="pymssql", trustedConnection=False):
    """
    Query a SQL Server with a SQL query, and saves the returned data into a CSV. Note that
    this does **not** return anything. It saves the data in a CSV file. This is designed to
    transfer a large amound of data over slow network. It seems more reliable to do this and read the
    CSV into a data frame, compared to sending the returned SQL data to a data frame.

    :param sql: the SQL query string
    :param csvFileName: the filename of the output CSV
    :param password: the password for SQl authentication
    :param server: the IP address of the SQl server, with port number.
    :param user: the SQL server logon
    :param database: a string of the SQL data base name
    :param verbose: print date time, etc.; default to True
    :param method: SQL library to use; default to "pymssql", can also be "pyodbc"
    :param trustedConnection: use Windows login if True; default to False.
    :return: nothing, or None
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
            logger.error("sql2csv:")
            logger.exception(e)
            exc_buffer = io.StringIO()
            traceback.print_exc(file=exc_buffer)
            logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
            conn = None
    elif method == "pyodbc":
        connectString=""
        if trustedConnection:
            connectString = \
                "DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={};DATABASE={};Trusted_Connection=yes;"\
                .format(server, database)
        else:
            connectString = \
                "DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={};DATABASE={};UID={};PWD={};"\
                .format(server, database, user, password)
        try:
            conn = pyodbc.connect(connectString)
        except Exception as e:
            logger.error("sql2csv:")
            logger.exception(e)
            exc_buffer = io.StringIO()
            traceback.print_exc(file=exc_buffer)
            logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
            conn = None
    else:
        # catch all
        conn = None

    if conn is None:
        if verbose:
            print(str(datetime.datetime.now()))
            print("sql2csv(): Connection failed to {}".format(server))
        return

    # Execute the query
    if verbose:
        print(str(datetime.datetime.now()))
        print("sql2csv(): Querying the SQL server:\n{}".format(sql))

    try:
        # Create a database cursor
        cursor = conn.cursor()
        cursor.execute(sql)
    except Exception as e:
        logger.error("sql2csv:")
        logger.exception(e)
        exc_buffer = io.StringIO()
        traceback.print_exc(file=exc_buffer)
        logger.error('Uncaught exception in worker process:\n%s', exc_buffer.getvalue())
        return

    # Go through the results row-by-row and write the output to a CSV file
    # (QUOTE_NONNUMERIC applies quotes to non-numeric data; change this to
    # QUOTE_NONE for no quotes.  See https://docs.python.org/2/library/csv.html
    # for other settings options)
    if verbose:
        print(str(datetime.datetime.now()))
        print("sql2csv(): Saving data to {}... ".format(csvFileName))
    with open(csvFileName, "w") as outfile:
        # writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer = csv.writer(outfile, delimiter='\t')
        for row in cursor:
            writer.writerow([str(s) for s in row])

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    if verbose:
        print(str(datetime.datetime.now()))
        print("sql2csv(): Close connection to SQL server {} ".format(server))
