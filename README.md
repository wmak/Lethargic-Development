Lethargic-Development
=====================
## Running the project (Assuming you have pip installed and a Ubuntu-like Environment)
These instructions assume a certain level of understanging of a unix environment
_For the first run_

1. `pip install Django==1.5.4`
- Install required Python Libraries
	- `pip install simplejson`
- `cd CMSReScheduler`
    - This directory should have a file called manage.py
- `python manage.py syncdb`
- `python manage.py loaddata initialdata.json`
- `python manage.py runserver`

_For future runs_
- `python manage.py syncdb`
- `python manage.py loaddata initialdata.json`
- `python manage.py runserver`
    - Now the CMSReScheduler will be running on your local environment on port 8000
