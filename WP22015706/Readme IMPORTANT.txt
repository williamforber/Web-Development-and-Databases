In order to run my website project please follow the instructions below:

Firstly, please make sure that the libraries: Flask, numpy, mysql-connector-python and bcrypt are installed, to do this run "pip list" in the command prompt.
Here are the commands to install the required libraries if the libraries are not installed:
"pip install Flask"
"pip install numpy"
"pip install mysql-connector-python"
"pip install bcrypt" //used for hashing paswords

Once these libraries are installed, run the command "python --version" to get the python version the libraries are installed on,
and select the correct python interpreter in vscode based on the version of python, see example "choosingInterpreter.png" for more info.

Secondly make sure that there are no schemas currently running on my SQL server with the name "horizontravels" see "My sql schemas.png” for more info,
and import the MySQL dump which is called "Horizon Travels Database". see "Importing MYSQL Dump.png"
Then using vs code, edit \WebsiteProject\dbconnect.py and change "passwd" to your root password for your MYSQL server see "Value to change.png" for more info

Finally inside vs code run \WebsiteProject\ProjectFlask.py

The website should now be fully operational,
use the credentials below to access the user accounts for the website:

Admin:

email address: testadmin@test.com
password: admin

Standard User:

email address: testuser@test.com
password: test

More users can be created through the signup page, but by default they will be standard users.

Extra info:

Source Code is at \WebsiteProject
Database dump is at \Horizon Travels Database

This project was written using python 3.11.3
