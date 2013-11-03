import utils.csvutils as csvutils
from django.shortcuts import render
from classes.models import Course
from classes.models import Room
from classes.models import CourseSchedule

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from forms import UploadCsv
import datetime
import time
import simplejson

def home(request):
	return render(request, 'test.html')

def import_csv_file(request, type):
''' NOTE: for now I have a single url for this. I can send them  each to a certain page if you guys prefer.
    This is still very much up for debate. Let me know what you all think
'''
    if type == 'schedule':
        form = UploadCsv(type, request.FILES)
        format = ['code', 'name', 'enrolment']
        parser_list = parse(request.FILES['file'], format, ',')
        update_courses(parser_list)
        return HttpResponse('The schedule file has been uploaded!')
    elif type == 'room':
        form = UploadCsv(type, request.FILES)
        format = ['code', 'name', 'building']
        parser_list = parse(request.FILES['file'], format, ',')
        update_rooms(parser_list)
        return HttpResponse('Room file has been uploaded!')
    elif type == 'department':
        form = UploadCsv(type, request.FILES)
        format = ['code', 'name']
        parser_list = parse(request.FILES['file'], format, ',')
        update_departments(parser_list)
        return HttpResponse('Department file has been uploaded!')
    else:
        return HttpResponse('Invalid Type!')

def csvimport(request):
    if request.method == 'POST':
        form = UploadCsv(request.POST, request.FILES)
        # The format is hardcoded and following the database's structure
        # because we don't know how the csv file will be yet. 
        # FIX that when we do.
        format = ['code', 'name', 'enrolment']    
        parsed = parse(request.FILES['file'], format, ',')
        update_courses(parsed)
        return HttpResponse('CSV file imported sucessfully.')
    else:
        form = UploadCsv()
    return render_to_response('csvimport.html', {'form': form}, context_instance=RequestContext(request))
    
def admin(request):
	return render(request, 'admin/index.html')

def admin_upload(request):
	return render(request, 'admin/upload.html')

#This view should receive two strings:
#1 - fields on which we should filter
#2 - values for each of the fields passed in 1.
#For Rooms we are considering the following fields:
# - capacity: an integer indicating the minimum capacity the room should have
# - availableon: the day to use checking if the room is available
# - availableat: the startTime to use when checking if the room is available
# - availablefor: the length to use when checking if the room is available
# - building: two character indicating the code for a building (IC, for example)
#The strings must be separated by '-'s.
#The order of the fields does not matter as long as the values are 
#in the same order.

#incomplete
def filterRooms(request, fields, values):
    if request.method == "GET":
        try:
            fList = fields.split('-')
            vList = values.split('-')
            qSet = Room.objects.all()
            for i in fList:
                if fList[i] == 'capacity':
                    qSet = qSet.filter(capacity__gt = int(vList[i]))
                elif fList[i] == 'building':
                    qSet = qSet.filter(code__startswith = vList[i])
                elif fList[i] == 'availableon':
                    qSet = qSet.filter(courseschedule__dayOfWeek = vList[i])
                elif fList[i] == 'availableat':
                    t = time.strptime(vList[i], "%H:%M")
                    dt = datetime.time(t.tm_hour, t.tm_min)
                    qSet = qSet.exclude(courseschedule__startTime = dt)
                    qSet = handleLength(qSet, dt);
                elif fList[i] == 'availablefor':
                    qSet = checkLengthOfAvailability(qSet, int(vList[i]))
            JSONSerializer = serializers.get_serializer("json")
            s = JSONSerializer()
            s.serialize(qSet)
            data = s.getvalue()
            return HttpResponse(content = data)
        except Exception as e:
            data = json.dumps("Error while room filtering")
            return HttpResponse(content = data)
    else:
        data = json.dumps("Unable to filter")
        return HttpResponse(content = data)

