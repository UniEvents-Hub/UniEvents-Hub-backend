# UniEvents-Hub-backend
## Creating and Using Virtual Environment
This project is built in a Python virtual environment so you need to create a virtual environment and activate it.
First CD into the root directory then run the following commands in the terminal.

**python3 -m venv myvenv**

If you are on Windows you have to open a terminal in the command prompt not Powershell and run the command

**myvenv\Scripts\activate**

If you are on Mac then run the following command

**source myvenv/bin/activate**

Once the virtual environment is activated, **for the first time only** you need to install all the dependencies by the following commands. Make sure you have that txt file in your current directory

**pip install -r requirements.txt**

*You don't need to install the dependencies after the first time but you must need to activate the virtual environment in order to run the project*

## Managing and Creating MySQL database

*For the first time, you need to follow these steps:*

1. You need to install MySQL and try to add MySQL workbench as well.
2. The **root** user should have the password as **"password"**, if you think you want to change the user and password then change the setting accordingly in the **settings.py** which is located inside the **src/rest_practice**.
3. Make a new database **mm802** in the MySQL server
4. Keep the server running or workbench running



## Running the server 

Then run the command:
**cd code**

*To create the database for the first time you need to run the following commands:*

**python manage.py makemigraions**

**python manage.py migrate**

## Create a superuser
**python manage.py createsuperuser**

## Run the server
To run the server run the command:
**python manage.py runserver**

