# UniEvents-Hub-backend
## Creating and Using Virtual Environment
This project is built in a python virtual environment so you need to create a virtual environment and activate it.
First CD into the root directory then run the following commands in the terminal.

**python3 -m venv myvenv**

If you are on Windows you have to open a terminal in the command prompt not Powershell and run the command

**myvenv\Scripts\activate**

If you are on Mac then run the following command

**source myvenv/bin/activate**

Once the virtual environment is activated, **for the first time only** you need to install all the dependencies by the following commands. Make sure you have that txt file in your current directory

**pip install -r requirements.txt**

* You don't need to install the dependencies after the first time but you must need to activate the virtual environment in order to run the project *



Then for the first time you need to follow this steps:

1. you need the MySQL installed, try to add MySQL workbench aswell
2. The root user should have the password, if you think you want to change the user and password then change the setting accordingly in the settings.py
3. Make a new database mm802 in the MySQL server
4. Keep the server running or workbench running

Then run the command:

cd src

To run the server run the command:

python manage.py runserver

