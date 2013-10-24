Lethargic-Development
=====================
## Running the project (Assuming you have pip installed and a Ubuntu-like Environment)
_For the first run_

1. "pip install Django==1.5.4"
- Install mysql
- Create a new user called "djangouser" with password "bulbasaur"
	- `CREATE USER 'djangouser'@'localhost' IDENTIFIED BY 'bulbasaur';`
	- `GRANT ALL PRIVILEGES ON *.* TO 'djangouser'@'localhost' WITH GRANT OPTION;`
	- `FLUSH PRIVILEGES;`
- Create a database in mysql called "CMSdb"
	- `CREATE DATABASE CMSdb;`
- "pip install MySQL-python"
- "cd CMSReScheduler"
    - This directory should have a file called manage.py
- "python manage.py runserver"

_For future runs_
- "python manage.py runserver"
Now the CMSReScheduler will be running on your local environment on port 8000
