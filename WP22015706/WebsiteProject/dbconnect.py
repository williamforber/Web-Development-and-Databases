# An extension of DBFUNC.py originally made by Zaheer, but with added support for specifiying a user to connect to the database
# Author: William Forber, StudentId:22015706
import mysql.connector
from mysql.connector import errorcode
# Global variables specifying the default values used to connect as a root user
databaseName = "horizontravels"
hostadress = "localhost"
username = "root"
# change this to your root password for your DBMS (MySql)
passwd = "ULB8mt$a8!LZkR"
# Function that uses the predefined values to connect to the databaes


def connectRoot():
    # try except statement attempting to connect to the database and handling exceptions appropraitly
    try:
        # connecting to the database
        conn = mysql.connector.connect(host=hostadress,
                                       user=username,
                                       password=passwd,
                                       database=databaseName)
    except mysql.connector.Error as err:
        # printing to the console an approprate message for common errors
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The username or password is invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The database name is invalid")
        else:
            print(err)
    else:

        return conn

# Function that uses paramaters to connect to the database as a different user


def connectOther(usr, key):
    # try except statement attempting to connect to the database and handling exceptions appropraitly
    try:
        # connecting to the database
        conn = mysql.connector.connect(host=hostadress,
                                       user=usr,
                                       password=key,
                                       database=databaseName)
    except mysql.connector.Error as err:
        # printing to the console an approprate message for common errors
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username or password is invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The database name is invalid")
        else:
            print(err)
    else:
        # checking wether the database is connected
        return conn
