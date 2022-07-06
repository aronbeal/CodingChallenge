import psycopg2
import os

def connect():
    """
    Returns a psycopg2 connection to the database.
    Relies on the proper shell env variables to be set to establish the connection.
    Please note that the db hostname relies on Docker aliasing.

    throws:
    RuntimeError: If the shell env vars for db connection are not defined: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
    or if the connection just can't be established.  This should be made more resilient for a real
    project.
    See https://peps.python.org/pep-0249/#id40 for more info.
    """
    hostname = 'db'
    dbname = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    pwd = os.getenv('POSTGRES_PASSWD')
    if dbname is None:
        raise RuntimeError("The db name could not be fetched as an environment variable, cannot continue")

    if user is None:
        raise RuntimeError("The db username could not be fetched as an environment variable, cannot continue")

    if pwd is None:
        raise RuntimeError("The db password could not be fetched as an environment variable, cannot continue")
    
    result = psycopg2.connect(dbname=dbname, user=user, password=pwd, host='db')
    if result is None:
        raise RuntimeError("Could not connect to the database.  Unknown reason")
    
    return result
