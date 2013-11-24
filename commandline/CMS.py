import requests
import ConfigParser
import sys

def setup():
	config = ConfigParser.ConfigParser()
	config.readfp(open("conf/config.ini"))
	global root_url
	global port
	root_url = config.get("Settings", "url")
	port = config.get("Settings", "port")

def get(request):
	r = requests.get(("http://%s:%s/%s" % (root_url, port, request)))
	if r.status_code == 200:
		return r.text

def put(request, body):
	pass

def course(method, code, body = None):
	result = "An Error has occured"
	if method == "get":
		result = get(("course/%s/") % code)
	return result

if __name__=="__main__":
	try:
		setup()
		if sys.argv[1].lower() == "course":
			if sys.argv[2].lower() == "get":
				final = course(sys.argv[2].lower(), sys.argv[3].upper())
			else:
				final = course(sys.argv[2].lower(), sys.argv[3].lower(), sys.argv[4])
	except IndexError:
		print "Incorrect number of variables. Your syntax must be as follows"
		print "\t python CMS.py <COMMAND> <METHOD> <PARAMETER>"
		print "\t The command parameter can be any of the following"
		print "\t\t course"
		print "\t\t\t followed by the type of request"
		print "\t\t\t followed by the course code"
		print "\t\t\t with the json body if you wish to make anything other than GET"
		print "\t\t\t ex. python CMS.py ANTB20H3S course put {\"department\" : \"Anthropology\"}"
	except Exception as e:
		print "An unknown error has occured: "
		print str(e)
	else:
		print final