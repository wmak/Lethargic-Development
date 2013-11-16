Lethargic-Development
=====================
## Running the project (Assuming you have pip installed and a Ubuntu-like Environment)
These instructions assume a certain level of understanging of a unix environment
_For the first run_

1. `pip install Django==1.5.4`
- install mysql
	- `sudo apt get mysql`
- Create a new user called "djangouser" with password "bulbasaur"
	- `CREATE USER 'djangouser'@'localhost' IDENTIFIED BY 'bulbasaur';`
	- `GRANT ALL PRIVILEGES ON *.* TO 'djangouser'@'localhost' WITH GRANT OPTION;`
	- `FLUSH PRIVILEGES;`
- Create a database in mysql called "CMSdb"
	- `CREATE DATABASE CMSdb;`
- `pip install MySQL-python`
- `cd CMSReScheduler`
    - This directory should have a file called manage.py
- `python manage.py runserver`

_For future runs_
- `python manage.py runserver`
Now the CMSReScheduler will be running on your local environment on port 8000

Automation Test Suite
=====================
## Setting up your automative suite (Assuming you have either knowledge of screen or a terminal with tabbing. As well as Firefox 25.0)

1. Install the test suite
	- `pip install py.saunter`
2. Change to the automation directory
	- `cd automation`
3. If you know how to use screens, start a new one and run the following command. Otherwise run this then open a new tab
	- `java -jar selenium-server-standalone.jar`
4. Make sure that within conf/saunter.ini that the base_url setting matches the location of the currently running server
5. Now you have selenium running start the autmoation test suite. Please don't use your computer while it is running as this may cause conflicting actions
	- `pysaunter -s -v -m regression`