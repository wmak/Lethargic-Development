import requests
import ConfigParser
import sys
try:
	import json
except ImportError:
	# Python 2.5
	import simplejson as json

def setup():
	config = ConfigParser.ConfigParser()
	config.readfp(open("conf/config.ini"))
	global root_url
	global port
	root_url = config.get("Settings", "url")
	port = config.get("Settings", "port")

def course(method, code, body = None):
	result = "An Error has occured"
	url = ("http://%s:%s/%s/%s" % (root_url, port, "course", code))
	exec(("r = requests.%s(url, data = body)") % method)
	return r.json()

def user(method, code, body = None):
	result = "An Error has occured"
	url = ("http://%s:%s/%s/%s" % (root_url, port, "user", code))
	exec(("r = requests.%s(url, data = body)") % method)
	return r.json()

def export(method, code, body = None):
	result = "An Error has occured"
	url = ("http://%s:%s/%s/%s" % (root_url, port, "export", code))
	r = requests.get(url, data = body)
	return r.json()

if __name__=="__main__":
	try:
		setup()
		if sys.argv[1].lower() == "course":
			if sys.argv[2].lower() == "get":
				final = course(sys.argv[2].lower(), sys.argv[3].upper())
			else:
				print sys.argv[4]
				final = course(ss.argv[2].lower(), sys.argv[3].upper(), sys.argv[4])
		elif sys.argv[1].lower() == "user":
			if sys.argv[2].lower() == "get":
				final = user(sys.argv[2].lower(), sys.argv[3].upper())
		elif sys.argv[1].lower() == "export":
				final = export(sys.argv[2].lower(), sys.argv[3].lower())
	except IndexError:
		print "Incorrect number of variables. Your syntax must be as follows"
		print "\t python CMS.py <COMMAND> <METHOD> <PARAMETER>"
		print "\t The command parameter can be any of the following"
		print "\t\t course"
		print "\t\t\t followed by the type of request"
		print "\t\t\t followed by the course code"
		print "\t\t\t with the json body if you wish to make anything other than GET"
		print "\t\t\t ex. python CMS.py ANTB20H3S course put {\"department\" : \"Anthropology\"}"
		print "\t\t user"
		print "\t\t\t followed by type of request"
		print "\t\t\t followed by the user_id"
		#todo
		#print "\t\t\t PUT: activates user"
		print "\t\t export"
		print "\t\t\t followed by `classes` to export that models data"
		print "\t\t\t or `all` to export all data"
	except Exception as e:
		print "An unknown error has occured: "
		print str(e)
	else:
		print final