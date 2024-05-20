// parts of these functions use parts of the date picker script from the lecture examples written by Zaheer.
// Author: William Forber, Student id:22015706
function checkBookingDate() {
    // getting the current date
    today = new Date();
    // splitting the date into the day month and year
    day = today.getDate();
    month = today.getMonth() + 1;
    year = today.getFullYear();

    // if the month is less than 10 add a zero behind it
    if (month < 10) {
        month = "0" + month;
    }
    // if the day is less than 10 add a zero behind it
    if (day < 10) {
        day = "0" + day
    }
    // defining the max day variable.
    var maxDay = day;
    // if the max day variable is greater than 28 then set to 28 because of feburary
    if (maxDay > 28) {
        maxDay = 28;
    }
    // defining the max month and year variables
    var maxMonth = month;
    var maxYear = year;
    // since bookings can be made 3 months in advance if the month greater than 9 once surpassing 12 set the year to increase by 1 and reset the month to 1 
    if (month > 9) {
        for (var i = 0; i < 3; i++) {
            // checking if at the end of the year
            if (maxMonth > 12) {
                maxMonth = 1;
                maxYear++;
            }
            maxMonth++
        }
    } else {
        // otherwise add 3 months to max month
        maxMonth = parseInt(maxMonth) + 3;
    }

    // if the max month is less than 10 add a zero behind it
    if (maxMonth < 10) {
        maxMonth = "0" + maxMonth
    }

    // if the max day is less than 10 add a zero behind it
    if (maxDay < 10) {
        maxDay = "0" + maxDay();
    }

    // combining the variables to create two date formats, the current date and the maximum date bookings can be made
    var formattedDate = year + "-" + month + "-" + day;
    var maxDate = maxYear + "-" + maxMonth + "-" + maxDay;
    // setting the date input so bookings cannot be made in the past
    document.getElementById('dateToLeave').min = formattedDate;
    // setting the date inputs maximum to never be beyond 3 months in the future
    document.getElementById('dateToLeave').max = maxDate;

}

function checkExpiryDate(){
    today = new Date();
    // splitting the date into the day month and year
    day = today.getDate();
    month = today.getMonth() + 1;
    year = today.getFullYear();

    // if the month is less than 10 add a zero behind it
    if (month < 10) {
        month = "0" + month;
    }
    // if the day is less than 10 add a zero behind it
    if (day < 10) {
        day = "0" + day
    }
    var formattedDate = year + "-" + month + "-" + day;
    document.getElementById('dateOfExpiry').min = formattedDate;
}