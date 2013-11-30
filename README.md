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

Commandline Interface
=====================
## Setting up the commandline interface. Also written in python.
1. Install necessary packages
	- `pip install requests`
2. Using the Commandline
	- either using the python or shell application the command when in the commandline directory is
		- `python CMS.py <PARAMETERS>`
		- `sh CMS.sh <PARAMETERS>` (or if you wish chmod the file first and you can use just `./CMS.sh`
	- As for parameters currently implemented there are three commands
		- course
			- course related commands
			- `get` returns all relevant information concerning the course
				- ex. `python CMS.py course get CSCC01H3`
			- `put` modifies the course depending on a json string you pass
				- The string should be in the following format:
					- `{"key":"value"}`
					- key can be one of 4 values
						- "name"
						- "enrolment"
						- "department"
						- "switch"
					- the value for "name", "enrolment" and "department" can be strings
					- for switch the value should be of the following format
						- `{"code" : "Course code to switch with", "section" : "the section to swap with"}`
				- ex. `python CMS.py course get CSCC01H3 "{\"name\":\"Software Engineering\"}"`
			- `post` creates a new course in the system
				- Requires a json string as well
					- format needs to be:
					- `{"code" : "new value", "name" : "new value", "enrolment" : "new value", "department" : "new value",}`
			- `delete` deletes a course from the system
				- no body is required, deletes the passed course code from the system
		- user
			- user related commands
			- `get` returns this users notifications
				- ex. `python CMS.py user get 1` #returns notifications for user with id=1
			- `put` moves notifications to a read state
				- ex. `python CMS.py user put 1 "[\"course 6 has been changed\"]`
		-filtering
			- filters courses, rooms and schedules related commands
			- 'get' returns all the information required
				- The string should be in the following format:
					- `{"key":"value"}`
					- For rooms, the keys and the values can be the following:
						- "capacity": an integer indicating the minimum capacity the room should have
						- "availableon": the day to use checking if the room is available
						- "availableat": the startTime to use when checking if the room is available, in the format "HH:MM"
						- "availablefor": the length (in minutes) to use when checking if the room is available
						- "building": two upper-case characters indicating the code for a building (IC, for example)
					- For courses, the keys and the values can be the following:
						- "roomcode": the code of the room in which the desired courses take place
						- "starttime": the desired startTimee for the courses, in the format "HH:MM"
						- "building": two upper-case characters indicating the code for a building (IC, for example).
					- For schedules, the keys and the values can be the following:
						- "roomcode": the room of which you want the schedule
						- "starttime": the starttime for which you want the scheduel, in the format "HH:MM"
						- building: two upper-case characters indicating the code for a building (IC, for example).
						- department: the characters that represent the abbreviation of a department (CSC, for example)
						- dayOfWeek: will be used to return the schedules of a specific day of the week


_Note_: This entire setup assumes a python 2.7 environment. If you're running 3 onwards don't expect anything to work.
