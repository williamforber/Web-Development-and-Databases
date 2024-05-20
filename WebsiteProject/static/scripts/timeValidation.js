// Author: William Forber, Student id:22015706
// A function which checks if the journey the user is trying to book is on the same day but in the past based on time
function validateTime() {
    // declaring a variable addZero defaulting to false
    var addZero = false;
    // getting the booking date from the form
    bookingDate = document.forms["continueBooking"]["date"].value;
    // getting the times from the form
    times = document.forms["continueBooking"]["times"].value;
    // regular expression used to get the time to leave from the times value
    timeToLeave = times.split(",")[0];
    // getting the current date
    currentDate = new Date();
    currentMonth = currentDate.getMonth() + 1;
    currentDay = currentDate.getDate();
    currentYear = currentDate.getFullYear();
    // if the month is less than 10 add a zero behind it
    if (currentMonth < 10) {
        currentMonth = "0" + currentMonth;
    }
    // if the day is less than 10 add a zero behind it
    if (currentDay < 10) {
        currentDay = "0" + currentDay;
    }
    // converting the current date to a string so the time can be grabbed from it
    currentDate = currentDate.toString();
    // formatting the date in the format Y-M-D as MYSQL uses this format
    formattedDate = currentYear + "-" + currentMonth + "-" + currentDay;
    // if the date of the booking is the same as the formatted date (today) the check weather the time to leave has already surpassed
    if (bookingDate == formattedDate) {
        // getting the current time from the date using regular expressions
        currentTime = currentDate.split(" ")[4];
        // getting the leave hour for comparison using regular expressions
        timeToLeaveComp = timeToLeave.split(":")[0];
        // getting the current hour for comparison using regular expressions
        currentTimeComp = currentTime.split(":")[0];
        // converting the variables into integers
        timeToLeaveComp = parseInt(timeToLeaveComp);
        currentTimeComp = parseInt(currentTimeComp);
        // checking if the current time surpasses the time to leave
        if (currentTimeComp > timeToLeaveComp) {
            // if so then output an error message
            document.getElementById("ErrorMessage").innerHTML = "Error: Your making a booking at a time in the past, please select another time or book on a different date.";
            return false;
        }
        // otherwise continue
        return true;
    }
    return true;
}
