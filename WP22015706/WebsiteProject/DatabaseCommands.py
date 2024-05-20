# Author: William Forber, StudentId:22015706
# A set of functions allowing for accessing/modifiying the database
import dbconnect
import bcrypt
from datetime import date, datetime, timedelta
import re
import numpy as np
import mysql.connector
from mysql.connector import errorcode

# function executing the statement use horizon travells


def useHorizonTravels():
    # defining the sql statment to be executed
    statement = "USE HorizonTravels;"
    # connecting to the database
    conn = dbconnect.connectRoot()
    # checking if the connection is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    # executing the sql statement
    dbcursor.execute(statement)


def isConnected(conn):
    # checking if the connection is not established
    if conn == None:
        # if connection not established then return an error otherwise continue
        return False
    return True


def createAccount(usr, email, passwd):
    useHorizonTravels()
    # providing the table name needed to be accessed
    tablename = 'useraccounts'
    # connecting to the database
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    statement = 'SELECT EmailAddress FROM ' + \
        tablename + ' WHERE EmailAddress = %s;'
    dataset = (email,)
    dbcursor.execute(statement, dataset)
    output = dbcursor.fetchall()
    if (output == []):
        # converting the inputted password into bytes in order to hash
        passwd = bytes(passwd, "utf-8")
        # generating a new salt for the password hash generation
        salt = bcrypt.gensalt()
        # hashing the password
        hashedpw = bcrypt.hashpw(passwd, salt)
        hashedpw = str(hashedpw)
        salt = str(salt)
        # adding the user
        statement = 'INSERT INTO '+tablename + ' (\
            UserName, EmailAddress, Password, Salt) VALUES (%s,%s,%s,%s);'
        # executing the statement and commiting the changes
        dataset = (usr, email, hashedpw, salt)
        dbcursor.execute(statement, dataset)
        conn.commit()
        return True
    conn.close()


def changeUserInfo(userId, infoToChange, newValue):
    useHorizonTravels()
    # connecting to the database
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    # if statement checking what user info needs to be changed and executing different statments depending on what needs to be changed
    if infoToChange == "name":
        statement = 'UPDATE UserAccounts SET UserName = %s WHERE UserId = %s'
        vals = (newValue, userId)
        dbcursor.execute(statement, vals)
        conn.commit()
        conn.close()
        return True
    elif infoToChange == "email":
        statement = 'UPDATE UserAccounts SET EmailAddress = %s WHERE UserId = %s'
        vals = (newValue, userId)
        dbcursor.execute(statement, vals)
        conn.commit()
        conn.close()
        return True
    elif infoToChange == "pass":
        # hashing the password
        password = bytes(newValue, "utf-8")
        salt = bcrypt.gensalt()
        hashedpw = bcrypt.hashpw(password, salt)
        # converting the hashed password and salt to a string so they can be stored in the database
        hashedpw = str(hashedpw)
        salt = str(salt)
        statement = 'UPDATE UserAccounts SET Password = %s, Salt = %s WHERE UserId = %s'
        vals = (hashedpw, salt, userId)
        dbcursor.execute(statement, vals)
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def getUserInfo(userId):
    useHorizonTravels()
    # SQL statement select all user info where the userId matches the input
    statement = "SELECT * FROM UserAccounts WHERE userId = %s;"
    # connecting to the database as a standard user
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    vals = (userId,)
    dbcursor = conn.cursor()
    # executing the statement
    dbcursor.execute(statement, vals)
    output = dbcursor.fetchall()
    # returning the output of the statement
    return output


def login(email, passwd):
    useHorizonTravels()
    # converting the provided password into bytes to allow for the password to be hashed
    key = bytes(passwd, "utf-8")
    # providing the table name used for the sql statements
    tablename = "useraccounts"
    # connecting to the database using the standard user with reduced permissions
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    statement = 'SELECT Salt FROM '+tablename+' WHERE EmailAddress = %s;'
    # executing the statement
    vals = (email,)
    dbcursor.execute(statement, vals)
    output = dbcursor.fetchone()
    if output == None:
        return False
    salt = bytes(output[0], "utf-8")
    salt = salt[2:len(salt) - 1]
    # hashing the password
    hashedpw = bcrypt.hashpw(key, salt)
    # first select statement selecting the hashed password from the databse for this user
    statement = 'SELECT Password FROM ' + \
        tablename + ' WHERE EmailAddress = %s;'
    # executing the statement
    vals = (email,)
    dbcursor.execute(statement, vals)
    output = dbcursor.fetchone()
    # converting the hashed password from the database into bytes for comparison
    checkoutput = bytes(output[0], "utf-8")
    checkoutput = checkoutput[2:len(checkoutput) - 1]
    # executing the next select statement selecting the user id of this user
    statement = 'SELECT UserId FROM ' + tablename + ' WHERE EmailAddress = %s;'
    vals = (email,)
    dbcursor.execute(statement, vals)
    output = dbcursor.fetchone()
    # setting the userid variable to the retreived user id
    userId = output[0]
    # if statement checking whether the hashed passwords match and returning true and the userId if they do match
    if checkoutput == hashedpw:
        statement = 'SELECT isAdmin FROM ' + tablename + ' WHERE userId = %s'
        vals = (userId,)
        dbcursor.execute(statement, vals)
        output = dbcursor.fetchone()
        isAdmin = output[0]
        conn.close()
        return True, userId, isAdmin
    else:
        conn.close()
        return False

# function for returning all flights with that origin and destination for a specific day


def getJourneys(origin, destination):
    useHorizonTravels()
    tablename = 'timetable'
    statement = 'SELECT * FROM '+tablename + \
        ' WHERE Origin = %s AND Destination = %s;'
    # connecting to the database
    vals = (origin, destination)
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    dbcursor.execute(statement, vals)
    timeTable = dbcursor.fetchall()
    conn.close()
    return timeTable


def executeStatement(statement):
    useHorizonTravels()
    # connecting to the database as a standard user
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    # defining a variable called special which is by defualt false
    special = False
    # list containing commands which do not output a table
    specialCommands = ['UPDATE', 'DELETE', 'INSERT', 'CREATE']
    # executing the statement
    try:
        dbcursor.execute(statement)
    except mysql.connector.Error as err:
        if err.errno == 1064:
            return "SyntaxError"
        else:
            return "Error"
    else:
        for i in range(len(specialCommands)):
            # using regular expressions to see if the statement contains any of the special commands
            if re.findall("^"+specialCommands[i], statement):
                # if so then the special variable is updated to true
                special = True
        # getting the table names
        tableDescription = dbcursor.description
        reccordNames = []
        # if the statement does not include special statements then add the table headers to reccord names
        if special != True:
            for i in range(len(dbcursor.description)):
                reccordNames.append(tableDescription[i][0])
        # getting the output from the table
        output = dbcursor.fetchall()
        # commit any changes
        conn.commit()
        # closing the connection
        conn.close()
        # returning the output variables
        return reccordNames, output, special


def listBookings(userId):
    useHorizonTravels()
    # SQL join statement looking at all bookings with there origin and destination that a user has made
    statement = 'SELECT Bookings.TimeId ,Bookings.UserId, Bookings.DateOfBooking, TimeTable.Origin, TimeTable.Destination, TimeTable.TimeToLeave, TimeTable.TimeToArrive, Bookings.DaysInAdvance,Bookings.isBusinessClass FROM bookings INNER JOIN TimeTable ON bookings.TimeId = TimeTable.TimeId WHERE UserId = %s AND DateOfBooking >= %s;'
    # connecting to the database as a standard user
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    # getting the current date so bookings made in the past do not show up
    currentDate = date.today()
    vals = (userId, currentDate)
    # executing the statement
    dbcursor.execute(statement, vals)
    # getting the output of the statement
    output = dbcursor.fetchall()
    # closing the connection
    conn.close()
    # if the output is empty return NO otherwise return the output
    if output == []:
        return "NO"
    return output


def genReport():
    useHorizonTravels()
    # creating a numpy array to store the timetable id with the total sales per trip
    monthlyTripSales = np.zeros((50, 2))
    # connecting to the database as a standard user
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    # getting the current date
    currentDate = date.today()
    # calculating the date one month before (29 days)
    thresholdDate = currentDate - timedelta(29)
    # converting the current date and the threshold date into strings
    currentDate = currentDate.strftime("%Y-%m-%d")
    thresholdDate = thresholdDate.strftime("%Y-%m-%d")
    # statment to get the time id with the days in advance, within the calculated dates
    statement = 'SELECT TimeId, DaysInAdvance,isBusinessClass FROM Bookings WHERE DateBookingMade > %s AND DateBookingMade <=%s'
    dbcursor = conn.cursor()
    vals = (thresholdDate, currentDate)
    # executing the statement
    dbcursor.execute(statement, vals)
    monthlyTotalSales = 0
    output = dbcursor.fetchall()
    # for loop to calculate the monthly sales figures
    for rows in output:
        monthlyTotalSales += getPrice(rows[0], rows[1], rows[2])
    statement = 'SELECT Bookings.TimeId ,Bookings.UserId, Bookings.DaysInAdvance, Bookings.DateBookingMade, TimeTable.Origin, TimeTable.Destination, TimeTable.TimeToLeave, TimeTable.TimeToArrive, Bookings.isBusinessClass FROM bookings INNER JOIN TimeTable ON bookings.TimeId = TimeTable.TimeId WHERE DateBookingMade > %s AND DateBookingMade <= %s;'
    vals = (thresholdDate, currentDate)
    dbcursor.execute(statement, vals)
    output = dbcursor.fetchall()
    # for loog to calculate the individual sales figues
    for rows in output:
        timeId = rows[0]
        monthlyTripSales[timeId][0] = timeId
        monthlyTripSales[timeId][1] += getPrice(timeId, rows[2], rows[8])
    statement = "SELECT * FROM TimeTable;"
    dbcursor.execute(statement)
    timeTable = dbcursor.fetchall()
    # statement to get the top customer (user who made the most bookings)
    statement = 'SELECT COUNT(UserAccounts.UserId), Bookings.UserId FROM UserAccounts INNER JOIN Bookings ON bookings.UserId = UserAccounts.UserId WHERE Bookings.DateBookingMade > %s AND Bookings.DateBookingMade <= %s GROUP BY UserAccounts.UserId ORDER BY COUNT(UserId) DESC;'
    dbcursor.execute(statement, vals)
    topUserId = dbcursor.fetchall()
    if (len(topUserId) >= 1):
        # statement to get the username of the top customer
        statement = 'SELECT UserName FROM UserAccounts WHERE UserId = %s;'
        vals = (topUserId[0][1],)
    dbcursor.execute(statement, vals)
    topUser = dbcursor.fetchone()
    statement = 'SELECT Bookings.TimeId ,Bookings.UserId, Bookings.DaysInAdvance, Bookings.isBusinessClass FROM bookings INNER JOIN TimeTable ON bookings.TimeId = TimeTable.TimeId WHERE DateBookingMade > %s AND DateBookingMade <= %s AND UserId = %s;'
    if (len(topUserId) >= 1):
        vals = (thresholdDate, currentDate, topUserId[0][1])
        dbcursor.execute(statement, vals)
        userBookings = dbcursor.fetchall()
        totalPrice = 0
        for rows in userBookings:
            totalPrice += getPrice(rows[0], rows[2], rows[3])
        # returning the required output variables
        return monthlyTotalSales, timeTable, monthlyTripSales, topUser, totalPrice
    return monthlyTotalSales, timeTable, monthlyTripSales, None, None


def getCancelPrice(timeId, date, userId):
    useHorizonTravels()
    # connecting to the database as a standard user
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    statement = "SELECT DaysInAdvance, isBusinessClass From Bookings WHERE UserId = %s AND TimeId = %s;"
    vals = (userId, timeId)
    # executing the above sql statement
    dbcursor.execute(statement, vals)
    output = dbcursor.fetchone()
    print(output)
    daysInAdvance = output[0]
    daysInAdvance = int(daysInAdvance)
    isBusinessClass = int(output[1])
    # getting the number of days the canclation is in advance and changing the price depending on that.
    dayBefore = countDays(date)
    if (dayBefore > 60):
        return 0
    elif (dayBefore <= 60 and dayBefore >= 30):
        return getPrice(timeId, daysInAdvance, isBusinessClass) * 0.5
    else:
        return getPrice(timeId, 0, isBusinessClass)


def countBookedSeats(timetableId, date):
    useHorizonTravels()
    tableName = 'Bookings'
    # statement to be executed
    statement = 'SELECT COUNT(TimeId) FROM '+tableName + \
        ' WHERE TimeId = %s AND DateOfBooking = %s;'
    # connecting to the database
    vals = (timetableId, date)
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    # executing the statement
    dbcursor.execute(statement, vals)
    seats = dbcursor.fetchone()
    # returning the number of bookings for that specific flight
    conn.close()
    return seats[0]


def getTimeTable():
    useHorizonTravels()
    # SQL statment selecting everything from the time table
    statement = 'SELECT * FROM TimeTable;'
    # connecting to the database as a standard user
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    # executing the statement
    dbcursor.execute(statement)
    # getting the output of the statement
    output = dbcursor.fetchall()
    # closing the connection
    conn.close()
    # returning the output
    return output


def getTimeTableId(origin, destination, timeToLeave):
    useHorizonTravels()
    tablename = 'timetable'
    # select statement getting the time id
    statement = 'SELECT * FROM ' + tablename + \
        ' WHERE Origin = %s AND Destination = %s AND TimeToLeave = %s;'
    # connecting to the database
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    vals = (origin, destination, timeToLeave)
    # executing the statement
    dbcursor.execute(statement, vals)
    rows = dbcursor.fetchone()
    timeId = rows[0]
    # returning the timeId
    conn.close()
    return timeId


def getPriceId(timeId):
    useHorizonTravels()
    # connecting to the database
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    # providing a select statement
    statement = 'SELECT PriceId FROM timetabletoprices WHERE TimeId = %s;'
    dbcursor = conn.cursor()
    vals = (timeId,)
    # executing the select statement
    dbcursor.execute(statement, vals)
    rows = dbcursor.fetchone()
    PriceId = rows[0]
    # returning the price id
    conn.close()
    return PriceId


def getPrice(timeId, daysBeforeBooking, experience):
    useHorizonTravels()
    # formatting price id to prevent sql injection
    priceId = getPriceId(timeId)
    # Defining the statement to be executed
    statement = 'SELECT Price FROM Prices Where priceId = %s;'
    # connecting to the database
    print("%s", statement)
    conn = dbconnect.connectRoot()
    # checking if connection to the database is established
    if (not (isConnected(conn))):
        # if not connected then return an error
        return "connection error"
    dbcursor = conn.cursor()
    vals = (priceId,)
    dbcursor.execute(statement, vals)
    row = dbcursor.fetchone()
    output = row[0]
    if experience == 1:
        output = output * 2
    # if statements applying discounts to the price if parameters are met
    if (daysBeforeBooking >= 80):
        conn.close()
        return output * 0.8
    elif (daysBeforeBooking >= 60 and daysBeforeBooking <= 79):
        conn.close()
        return output * 0.9
    elif (daysBeforeBooking >= 45 and daysBeforeBooking <= 59):
        conn.close()
        return output * 0.95
    # validation making sure that you cannot book a flight in the past
    elif (daysBeforeBooking < 0):
        conn.close()
        return None
    else:
        conn.close()
        return output


def countDays(bookDate):
    useHorizonTravels()
    # getting the current date
    currentDate = date.today()
    # converting to string
    currentDate = str(currentDate)
    # converting the booking date into a date time format
    bookDate = datetime.strptime(bookDate, "%Y-%m-%d")
    # converting the current date into a date time format
    currentDate = datetime.strptime(currentDate, "%Y-%m-%d")
    numberOfDays = bookDate - currentDate
    # converting the number of days to a string
    numberOfDays = str(numberOfDays)
    # finding the first string with any numbers of 0-9 using regular expressions, this is the number of days
    output = re.findall("-*[0-9]*", numberOfDays)[0]
    # returning the number of days between the two dates
    return int(output)


def getBooking(userId, date, timeId):
    useHorizonTravels()
    # checking if the user id inputted is invalid
    if not (userId == None):
        tablename = 'Bookings'
        # SQL statment that selects everything from bookings where the user id, date and time id match with the inputted paramaters
        statement = 'SELECT * FROM '+tablename + \
            ' WHERE UserId = %s  AND  DateOfBooking = %s AND TimeId = %s;'
        conn = dbconnect.connectRoot()
        # checking if connection to the database is established
        if (not (isConnected(conn))):
            # if not connected then return an error
            return "connection error"
        vals = (userId, date, timeId)
        dbcursor = conn.cursor()
        dbcursor.execute(statement, vals)
        output = dbcursor.fetchone()
        if (output == None):
            conn.close()
            return False
        conn.close()
        return output
    else:
        conn.close()
        return "Error"


def createBooking(origin, destination, userId, bookDate, timeToLeave, experience):
    useHorizonTravels()
    daysInAdvance = countDays(bookDate)
    if (daysInAdvance > 90 and daysInAdvance < 0):
        print("Error bookings need to be made at most 3 months in advance!\n")
        print("And cannot be made before the current date")
    else:
        if not (userId == None):
            currentDate = date.today()
            currentDate = currentDate.strftime("%Y-%m-%d")
            # getting the userid to insert into the bookings table
            userId = userId
            tablename = "bookings"
            # checking whether the same user is trying to make multiple bookings for the exact same trip
            if not (getBooking(userId, bookDate, getTimeTableId(origin, destination, timeToLeave))):
                # getting the desired flight
                timetableid = getTimeTableId(origin, destination, timeToLeave)
                # select statement to be executed
                statement = 'INSERT INTO ' + tablename + \
                    ' (UserId, PriceId, DateOfBooking, DaysInAdvance, DateBookingMade,isBusinessClass,TimeId) VALUES(%s,%s,%s,%s,%s,%s,%s);'
                # connecting to the database
                conn = dbconnect.connectRoot()
                # checking if connection to the database is established
                if (not (isConnected(conn))):
                    # if not connected then return an error
                    return "connection error"
                dbcursor = conn.cursor()
                # executing the statement and commiting it
                priceId = getPriceId(getPriceId(timetableid))
                vals = (userId, priceId, bookDate,
                        daysInAdvance, currentDate, experience, timetableid)
                dbcursor.execute(statement, vals)
                conn.commit()
                conn.close()
            else:
                return "Multiple booked"
        else:
            print("The username or password is incorrect")


def deleteBooking(timeId, date, userId):
    useHorizonTravels()
    # checking whether the login credentials are valid
    if (userId):
        # delete statement to be executed
        statement = 'DELETE FROM Bookings WHERE timeId = %s AND DateOfBooking = %s AND userId = %s;'
        vals = (timeId, date, userId)
        # connecting to the database as a standard user
        conn = dbconnect.connectRoot()
        # checking if connection to the database is established
        if (not (isConnected(conn))):
            # if not connected then return an error
            return "connection error"
        dbcursor = conn.cursor()
        # executing and commiting the delete statement
        dbcursor.execute(statement, vals)
        conn.commit()
        conn.close()
        return True
    else:
        return False


def deleteAccount(userId):
    useHorizonTravels()
    # checking wheather login credentials are valid
    if (userId):
        # connecting to the database
        conn = dbconnect.connectRoot()
        # checking if connection to the database is established
        if (not (isConnected(conn))):
            # if not connected then return an error
            return "connection error"
        tablename = 'useraccounts'
        cursor = conn.cursor()
        # defining the delete statement
        deleteStatement = 'DELETE FROM ' + tablename + ' WHERE UserId = %s;'
        vals = (userId,)
        # executing the delete statement and committing it
        cursor.execute(deleteStatement, vals)
        conn.commit()
        conn.close()
    else:
        print("The username or password is incorrect")
