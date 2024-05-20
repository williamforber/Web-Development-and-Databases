To run my website project please follow the instructions below:

Firstly, please ensure that the libraries: Flask, numpy, mysql-connector-python and bcrypt are installed, to do this run "pip list" in the command prompt.
Here are the commands to install the required libraries if the libraries are not installed:
"pip install Flask"
"pip install numpy"
"pip install mysql-connector-python"
"pip install script" //used for hashing passwords


Secondly, make sure that there are no schemas currently running on my SQL server with the name "horizontravels"
and import the MySQL dump located at \Horizon Travels Database".
Then using vs code, edit \WebsiteProject\dbconnect.py and change "passwd" to your root password for your MYSQL server.

Finally inside vs code run \WebsiteProject\ProjectFlask.py

The website should now be fully operational,
use the credentials below to access the user accounts for the website:

Admin:

email address: testadmin@test.com
password: admin

Standard User:

email address: testuser@test.com
password: test

More users can be created through the signup page, but they will be standard users by default.

Extra info:

The Source Code is at \WebsiteProject
The MySQL Database dump is at \Horizon Travels Database

This project was written using Python 3.11.3 but should work for the latest versions
