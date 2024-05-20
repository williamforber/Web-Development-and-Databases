# Author: William Forber, StudentId:22015706
# The main py file to run my website (rendering templates, containing all routes)
from flask import Flask, render_template, request, session
from functools import wraps
import DatabaseCommands
from datetime import datetime
import re
app = Flask("ProjectFlask")

# wrapper checking weather the user is logged in


def isLoggedIn(f):
    @wraps(f)
    def check(*args, **kwargs):
        # checking weather the user id is actually being used
        if session.get('userId'):
            return f(*args, **kwargs)
        else:
            # if not being used the user is not logged in output error
            errormessage = "You need to be logged in first to do that"
            return render_template("loginPage.html", errormessage=errormessage)
    return check

# wrapper checking wether the user is an admin


def isAdmin(f):
    @wraps(f)
    def check(*args, **kwargs):
        # checking if the isAdmin flag is 1
        if session.get('isAdmin') == 1:
            return f(*args, **kwargs)
        else:
            # if not 1 then user is a standard user
            errormessage = "Access denied user not administrator!"
            return render_template("loginPage.html", errormessage=errormessage)
    return check

# route to the main page


@app.route('/')
def index():
    # returning the home page
    return render_template("index.html")


@app.route('/Bookings')
# checking wether the user is logged in
@isLoggedIn
def bookings():
    # getting the bookings for the user
    bookings = DatabaseCommands.listBookings(session.get('userId'))
    # checking if connection to the database is established
    if (bookings == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    if bookings == "NO":
        return render_template("bookings.html", error=True)
    # outputting the bookings to the user
    return render_template("bookings.html", bookings=bookings)


@app.route('/AdminCommands')
# checking weather the user is logged in and is an admin
@isAdmin
@isLoggedIn
def adminCommands():
    return render_template("adminCommands.html")


@app.route('/GenReport')
# checking weather the user is logged in and is an admin
@isAdmin
@isLoggedIn
def genReport():
    # calling the generate report subroutine
    report = DatabaseCommands.genReport()
    # checking if connection to the database is established
    if (report == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    # formatting the sales figures so they are displayed in 2 decimal places
    totalSales = format(report[0], '.2f')
    # defining the variables to be sent to the webpage
    timeTable = report[1]
    tripSales = report[2]
    topUserRevenue = report[4]
    if (topUserRevenue != None):
        topUserRevenue = format(topUserRevenue, '.2f')
        topUser = str(report[3])
        topUser = topUser[1:len(topUser) - 2]
        # returning the genReport.html with the variables
        return render_template("GenReport.html", totalSales=totalSales, timeTable=timeTable, tripSales=tripSales, topUser=topUser, topUserRevenue=topUserRevenue)
    return render_template("GenReport.html", totalSales=totalSales, timeTable=timeTable, tripSales=tripSales)


@app.route('/AlterDatabase')
# checking weather the user is logged in and is an admin
@isAdmin
@isLoggedIn
def alterDatabase():
    return render_template("AlterDatabase.html")


@app.route('/Account')
# checking weather the user is logged in
@isLoggedIn
def account():
    userInfo = []
    # getting the user info from the database
    info = DatabaseCommands.getUserInfo(session.get('userId'))
    # checking if connection to the database is established
    if (info == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    for rows in info:
        userInfo.append(rows[1])
        userInfo.append(rows[2])
        pass
    # returning the account information
    return render_template("Account.html", userInfo=userInfo)


@app.route('/editAccount', methods=['POST'])
# checking weather the user is logged in
@isLoggedIn
def editAccount():
    # getting the desired information to edit
    infoToChange = request.form['info']
    if infoToChange == "name":
        return render_template("editinfo.html", info=infoToChange)
    elif infoToChange == "email":
        return render_template("editinfo.html", info=infoToChange)
    elif infoToChange == "pass":
        return render_template("editinfo.html", info=infoToChange)
    else:
        # just in case a user somehow makes infoToChange invalid
        errormessage = "Operation not supported"
        return render_template("Account.html", errormessage=errormessage)


@app.route('/DeleteAccount')
# checking wether the user is logged in
@isLoggedIn
def deleteAccount():
    return render_template("deleteAccount.html")


@app.route('/CompleteDelete', methods=['POST'])
# checking if the user is logged in
@isLoggedIn
def completeDelete():
    # getting the passwords from the form
    passwd = request.form['pass']
    passwd2 = request.form['pass2']
    # defining the error message in case it needs to be used
    errormessage = "Error: Inputted passwords do not match!"
    # checking wether the passwords match
    if (passwd == passwd2):
        # if they match call delete account
        delete = DatabaseCommands.deleteAccount(session.get('userId'))
        # checking if connection to the database is established
        if (delete == "connection error"):
            # if not connected output an error message
            errormsg = "Error: Connection to the database could not be established please try again later!"
            return render_template("index.html", errormessage=errormsg)
        # removing the sessions
        session.pop('userId', None)
        session.pop('isAdmin', None)
        # defining a message to be displayed in editSuccess
        message = "We are sorry to see you go, thank you for using our services!"
        # returning the message
        return render_template("editSuccess.html", message=message)
    # returning the error message
    return render_template("deleteAccount.html", errormessage=errormessage)


@app.route('/DeleteBooking')
# checking if the user is logged in
@isLoggedIn
def deleteBooking():
    # getting all of the bookings the user has made
    bookings = DatabaseCommands.listBookings(session.get('userId'))
    # checking if connection to the database is established
    if (bookings == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    # returning bookings.html with the deleting variable set to true
    return render_template("bookings.html", bookings=bookings, deleting=True)


@app.route('/cancelPrice', methods=['POST'])
@isLoggedIn
def cancelPrice():
    # getting the time and date from the form
    timeAndDate = request.form['select']
    # using regular expressions as values are seperated by commas
    timeId = re.split(",", timeAndDate)[0]
    date = re.split(",", timeAndDate)[1]
    # getting the cancelation fee
    price = DatabaseCommands.getCancelPrice(
        timeId, date, session.get('userId'))
    # checking if connection to the database is established
    if (price == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    # formatting the cancelation fee so it is rounded to 2 decimal places
    price = format(price, '.2f')
    price = float(price)
    # returning the price to the user
    return render_template("cancelPrice.html", price=price, timeId=timeId, date=date)


@app.route('/cancelSuccess', methods=['POST'])
# checking if the user is logged in
@isLoggedIn
def cancelSuccess():
    # getting the timeId of the booking and the date of booking from the form
    timeId = request.form['timeTableId']
    date = request.form['dateOfTravel']
    # deleting the booking
    success = DatabaseCommands.deleteBooking(
        timeId, date, session.get('userId'))
    # checking if connection to the database is established
    if (success == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    if success == True:
        # if deleted return a conformation message to the user
        return render_template("editSuccess.html", message="You have successfully canceled your booking!")
    # otherwise return an error message
    return render_template("canclePrice.html", errormessage="Error: Unable to delete booking please try again later!")


@app.route('/processEdit', methods=['POST'])
# checking wether the user is logged in
@isLoggedIn
def processEdit():
    # getting the user information to change from the form
    infoToChange = request.form['infoToChange']
    # defining the success message
    message = "Account details successfully editied"
    # if statments going through all of the possible details to edit and changing the user details
    if (infoToChange == "name"):
        if (request.form['user1'] == request.form['user2']):
            info = DatabaseCommands.changeUserInfo(session.get(
                'userId'), infoToChange, request.form['user1'])
            # checking if connection to the database is established
            if (info == "connection error"):
                # if not connected output an error message
                errormsg = "Error: Connection to the database could not be established please try again later!"
                return render_template("index.html", errormessage=errormsg)
            return render_template("editSuccess.html", message=message)
        else:
            errormessage = "Error: Inputted usernames do not match!"
            return render_template("editinfo.html", errormessage=errormessage, info=infoToChange)
    elif (infoToChange == "email"):
        if (request.form['email1'] == request.form['email2']):
            info = DatabaseCommands.changeUserInfo(session.get(
                'userId'), infoToChange, request.form['email1'])
            # checking if connection to the database is established
            if (info == "connection error"):
                # if not connected output an error message
                errormsg = "Error: Connection to the database could not be established please try again later!"
                return render_template("index.html", errormessage=errormsg)
            return render_template("editSuccess.html",  message=message)
        else:
            errormessage = "Error: Inputted email addresses do not match!"
            return render_template("editinfo.html", errormessage=errormessage, info=infoToChange)

    elif (infoToChange == "pass"):
        if (request.form['pass1'] == request.form['pass2']):
            info = DatabaseCommands.changeUserInfo(session.get(
                'userId'), infoToChange, request.form['pass1'])
            # checking if connection to the database is established
            if (info == "connection error"):
                # if not connected output an error message
                errormsg = "Error: Connection to the database could not be established please try again later!"
                return render_template("index.html", errormessage=errormsg)
            return render_template("editSuccess.html",  message=message)
        else:
            errormessage = "Error: Inputted passwords do not match!"
            return render_template("editinfo.html", errormessage=errormessage, info=infoToChange)


@app.route('/Logout')
# checking weather the user is logged in
@isLoggedIn
def logout():
    # removing the created sessions
    session.pop('userId', None)
    session.pop('isAdmin', None)
    return render_template("index.html")


@app.route('/Login')
def login():
    # displaying the login page
    return render_template("LoginPage.html")


@app.route('/ProcessLogin', methods=['POST'])
def processLogin():
    # getting the email address and password form the form
    email = request.form['email']
    passwd = request.form['password']
    loginInfo = DatabaseCommands.login(email, passwd)
    # checking if connection to the database is established
    if (loginInfo == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("loginPage.html", errormessage=errormsg)
    # checking wheather these credentials are valid
    if loginInfo:
        # getting the userId and is admin flags from the database
        loginDetails = DatabaseCommands.login(email, passwd)
        # creating new sessions used to tell if the user is logged in and is the user a admin
        session['userId'] = loginDetails[1]
        session['isAdmin'] = loginDetails[2]
        # returning the user to the home page
        return index()
    else:
        errormessage = "Error: Invalid email address or password please try again!"
        return render_template("loginPage.html", errormessage=errormessage)


@app.route('/executeStatementDefined', methods=['POST'])
# checking weather the user is logged in and is an administrator
@isAdmin
@isLoggedIn
def executeStatementDefined():
    table = request.form['tables']
    statement = 'SELECT * FROM %s' % (table)
    info = DatabaseCommands.executeStatement(statement)
    output = info[1]
    executed = False
    for rows in output:
        executed = True
        lengthOutput = len(rows)
    if (executed == True):
        return render_template("AlterDatabase.html", output=output, reccordNames=info[0], lengthNames=len(info[0]), lengthOutput=lengthOutput)
    else:
        return render_template("AlterDatabase.html", output=output, reccordNames=info[0], lengthNames=len(info[0]), errormessage="Table empty!")


@app.route('/executeStatement', methods=['POST'])
# checking weather the user is logged in and is an administrator
@isAdmin
@isLoggedIn
def executeStatement():
    statement = request.form['statement']
    # executing the statement and getting the reccord names and the output
    tableInfo = DatabaseCommands.executeStatement(statement)
    reccordNames = tableInfo[0]
    # checking if connection to the database is established
    if (reccordNames == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    elif (reccordNames == "S"):
        # if syntax is wrong output an error message
        errormsg = "Error: Inputted syntax is invalid!"
        return render_template("AlterDatabase.html", errormessage=errormsg)

    output = tableInfo[1]
    # special used for statements like insert into
    special = tableInfo[2]
    if (not special):
        executed = False
        lengthNames = len(reccordNames)
        for rows in output:
            executed = True
            lengthOutput = len(rows)
        # checking if the loop has executed
        if (executed == True):
            # returning the result to the admin
            return render_template("AlterDatabase.html", output=output, reccordNames=reccordNames, lengthNames=lengthNames, lengthOutput=lengthOutput)
        return render_template("AlterDatabase.html", output=output, reccordNames=reccordNames, lengthNames=lengthNames, errormessage="Table empty!")
    return render_template("AlterDatabase.html")


@app.route('/LoginPass', methods=['POST'])
def loginPass():
    # getting required data from the form
    origin = request.form['origin']
    destination = request.form['destination']
    bookDate = request.form['date']
    times = request.form['times']
    experience = request.form['experience']
    # using regular expressions as times has different values seperated by commas
    timeToLeave = re.split(",", times)[0]
    timeToArrive = re.split(",", times)[1]
    timeId = re.split(",", times)[2]
    price = request.form['price']
    # counting the number of seats booked for the requested flight
    numSeats = DatabaseCommands.countBookedSeats(timeId, bookDate)
    # checking if connection to the database is established
    if (numSeats == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("loginPass.html", errormessage=errormsg)
    if (numSeats >= 120):
        # if the flight is fully booked output an error message
        bookingInfo = [origin, destination, bookDate, price, experience]
        errormessage = "Error: This flight is fully booked please select another flight or book this flight on a different date!"
        trips = DatabaseCommands.getJourneys(origin, destination)
        return render_template("prices.html", formData=bookingInfo, errormessage=errormessage, journeys=trips, prices=price)
    # otherwise continue with booking
    bookingInfo = [origin, destination, bookDate,
                   timeToLeave, timeToArrive, price, experience]
    if session.get('userId'):
        return render_template("payment.html", bookingInfo=bookingInfo, userId=session.get('userId'))
    # putting all data fetched from the form into an array and redirecting the user to a new page to process the data
    return render_template("LoginPass.html", bookingInfo=bookingInfo)


@app.route('/payment', methods=['POST'])
def payment():
    # getting required data from the form
    origin = request.form['origin']
    destination = request.form['dest']
    date = request.form['date']
    email = request.form['email']
    password = request.form['passwd']
    timeToLeave = request.form['timeToLeave']
    timeToArrive = request.form['timeToArrive']
    price = request.form['price']
    experience = request.form['experience']
    # putting all data fetched from the form into an array.
    bookingInfo = [origin, destination, date,
                   timeToLeave, timeToArrive, price, experience]
    # Checking wheathre the provided credentials are valid
    loginInfo = DatabaseCommands.login(email, password)
    # checking if connection to the database is established
    if (loginInfo == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("payment.html", errormsg=errormsg)
    if loginInfo:
        # if valid return the user Id and the array containing data needed to be passed to a new page to process the data
        loginDetails = DatabaseCommands.login(email, password)
        session['userId'] = loginDetails[1]
        session['isAdmin'] = loginDetails[2]
        userId = loginDetails[1]
        return render_template("payment.html", bookingInfo=bookingInfo, userId=userId)
    else:
        # if not valid then redirect the user to the same page containing an error message so the user can try again.
        errormsg = "invalid email address or password please try again!"
        return render_template("LoginPass.html", errormsg=errormsg, bookingInfo=bookingInfo)


@app.route('/bookingConformation', methods=['POST'])
@isLoggedIn
def bookingConformation():
    # getting required data from the form
    origin = request.form['origin']
    destination = request.form['dest']
    date = request.form['date']
    userId = request.form['userId']
    timeToLeave = request.form['timeToLeave']
    timeToArrive = request.form['timeToArrive']
    experience = request.form['experience']
    # Creating the booking in the database using all of the data gathered by the forms
    booking = DatabaseCommands.createBooking(
        origin, destination, userId, date, timeToLeave, experience)
    # checking if connection to the database is established
    if (booking == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    if booking == "Multiple booked":
        errormessage = "Error: You cannot book the exact same flight multiple times, please book another flight!"
        return render_template("index.html", errormessage=errormessage)
    bookingInfo = [origin, destination, date, timeToLeave, timeToArrive]
    # redirecting the user to a conformation page containing the booking info
    return render_template("bookingConformation.html", bookingInfo=bookingInfo)


@app.route('/SignUp', methods=['POST'])
def createAccount():
    # getting required data from the form
    userName = request.form['userName']
    emailAddress = request.form['email']
    passwd = request.form['password']
    passwd2 = request.form['re-enterPassword']
    # checking wether the provided user passwords match
    if (passwd == passwd2):
        account = DatabaseCommands.createAccount(
            userName, emailAddress, passwd)
        # checking if connection to the database is established
        if (account == "connection error"):
            # if not connected output an error message
            errormsg = "Error: Connection to the database could not be established please try again later!"
            return render_template("signUpPage.html", errormessage=errormsg)
        if account:
            # if the account is created redirect the user to the login page and output a message
            message = "You have successfully created an account!"
            return render_template("loginPage.html", message=message)
        else:
            # if the account cannot be created because there is anouther user with the same information output an errormessage
            errormessage = "Error: The same user already exists!"
            return render_template("signUpPage.html", errormessage=errormessage)
    else:
        # if the passwords do not match then output an error message
        errormessage = "Error: passwords do not match!"
        return render_template("signUpPage.html", errormessage=errormessage)


@app.route('/displayTimeTable')
def displayTimeTable():
    # getting the time table from the database
    timetable = DatabaseCommands.getTimeTable()
    # checking if connection to the database is established
    if (timetable == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    # returning the time table to the user
    return render_template("TimeTable.html", timetable=timetable)

# rendering signUpPage.html for the route /Login/SignUp


@app.route('/Login/SignUp')
def signUp():
    return render_template("signUpPage.html")

# rendering help.html for the route /Help


@app.route('/Help')
def help():
    return render_template("help.html")

# rendering aboutUs.html for the route /AboutUs


@app.route('/AboutUs')
def aboutUs():
    return render_template("aboutUs.html")

# rendering privacy.html for the route /PrivacyPolicy


@app.route('/PrivacyPolicy')
def privacyPolicy():
    return render_template("privacy.html")


@app.route('/getPrices', methods=['POST'])
def getPrices():
    # getting required data from the form
    origin = request.form['start']
    destination = request.form['end']
    bookDate = request.form['date']
    experience = request.form['travelClass']
    inputData = [origin, destination, bookDate, experience]
    bookDate = datetime.strptime(bookDate, "%Y-%m-%d")
    # checking wheather the booking is made on an invalid day (sunday)
    if bookDate.weekday() == 6:
        # returning an error message to the user
        errormsg = "Error: booking's cannot be made on a Sunday!"
        return render_template("index.html", errormessage=errormsg)
    # getting the valid trips from the database using the form data
    trips = DatabaseCommands.getJourneys(origin, destination)
    # checking if connection to the database is established
    if (trips == "connection error"):
        # if not connected output an error message
        errormsg = "Error: Connection to the database could not be established please try again later!"
        return render_template("index.html", errormessage=errormsg)
    bookDate = bookDate.strftime("%Y-%m-%d")
    # checking wheather the combination of origin and destination exists in the database
    if len(trips) == 0:
        # returning an error message to the user
        errormsg = "Error: There is no journey available between the requested origin and destination!"
        return render_template("index.html", errormessage=errormsg)
    # getting the price of the trip from the database
    cost = DatabaseCommands.getPrice(
        trips[0][0], DatabaseCommands.countDays(bookDate), int(experience))
    # checking wheather the date specified from the user is in the past
    if cost == None:
        # returning an error message to the user
        errormsg = "Error: You cannot make a booking for the past"
        return render_template("index.html", errormessage=errormsg)

    # rounding the cost to 2 decimal places
    cost = format(cost, '.2f')
    # redirecting the user to a page which will take in all of the data and let the user choose which booking to procede with
    return render_template("prices.html", journeys=trips, prices=cost, formData=inputData)


@app.route('/GenQrCode', methods=['POST'])
@isLoggedIn
def genQrCode():
    # getting the information from the form
    booking = request.form['booking']
    # since the information is split with forms regular expressions are used to fetch different values
    origin = re.split(',', booking)[0]
    destination = re.split(',', booking)[1]
    date = re.split(',', booking)[2]
    time = re.split(',', booking)[3]
    timeId = re.split(',', booking)[4]
    daysBeforeBooking = re.split(',', booking)[5]
    daysBeforeBooking = int(daysBeforeBooking)
    experience = re.split(',', booking)[6]
    experience = int(experience)
    # getting the current user id
    userId = session.get('userId')
    # using the user id to get the email address of the user
    emailAddress = DatabaseCommands.executeStatement(
        "SELECT EmailAddress FROM UserAccounts WHERE userId = %s;" % (userId))
    price = DatabaseCommands.getPrice(timeId, daysBeforeBooking, experience)
    # creating a list containing all information required to be sent back
    bookingInfo = [origin, destination, date,
                   time, emailAddress, price, experience]

    # returning the qr code template sending it booking info
    return render_template("QrCode.html", bookingInfo=bookingInfo)


app.secret_key = '9KGvA3qCTP3%J$qhV!4u@'
app.run(debug=True)
