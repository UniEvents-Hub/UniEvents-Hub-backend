# UniEvents-Hub-backend
This project is built in a python virtual environment so you need to create an virtual environment and activate it.
First CD into the root directory then run the following commands in the terminal.

python3 -m venv myvenv

If you are on windows you have open a terminal in command prompt not powershell and run the command

myvenv\Scripts\activate

If you are on Mac then run the following command

source myvenv/bin/activate

Once the virtual environment is activated, for the first time only you need to install all the dependencies by the following commands. Make sure you have that txt file in your current directory

pip install -r requirements.txt

You don't need to install the dependencies after the first time but you must need to activate the virtual environment in order to run the project.

Then run the command:

cd src

To run the server run the command:

python manage.py runserver

