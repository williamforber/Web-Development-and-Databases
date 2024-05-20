// Author: William Forber, Student id:22015706
// A function which uses a library to generate a qr code with the data provided
function genQrCode() {
    // getting the origin, destination, date, timeToLeave and email values from the hidden form
    var origin = document.forms["booking"]["origin"].value;
    var destination = document.forms["booking"]["destination"].value;
    var date = document.forms["booking"]["date"].value;
    var timeToLeave = document.forms["booking"]["timeToLeave"].value;
    var email = document.forms["booking"]["email"].value;
    var price = document.forms["booking"]["price"].value;
    var isBusinessClass = document.forms["booking"]["experience"].value;
    // if isBusinessclass is 1 then set isBusiness class to Business otherwise set to economy
    if(isBusinessClass == 1){
        isBusinessClass = "Business";
    }else{
        isBusinessClass = "Economy";
    }
    // using a custom library QRCode.js to generate and display the qr code using the above information
    new QRCode(document.getElementById("code"), "Email Address: " + email.substring(3, email.length - 4) + "\nOrigin: " + origin + "\nDestination: " + destination + "\nDate: " + date + "\nTime to leave: " + timeToLeave + "\nPrice: " + price+ "\nClass: "+isBusinessClass);
}