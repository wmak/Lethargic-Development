import utils.csvutils as csvutils
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from forms import UploadCsv
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

#This view should receive three strings:
#1 - which model will be used, shoulb be in the plural for consistency
#2 - fields on which we should filter
#3 - values for each of the fields passed in 1.
#The strings must be separated by '-'s.
#The order of the fields does not matter as long as the values are 
#in the same order.
def filter(request, model, fields, values): 
    if request.method == "GET":
        try:
            fList = fields.split('-')
            vList = values.split('-')
            qSet = []
            if(fList.length != vList.length):
                data = json.dumps("Unable to filter. Number of fields does not match the number of values.")
                return HttpResponse(content = data)
            if model == "rooms":
                qSet = filterRooms(fList, vList)
            elif model == "courses":
                qSet = filterCourses(fList, vList)
            else:
                data = json.dumps("Unable to filter. No such model named %s" % (model))
                return HttpResponse(content = data)
            JSONSerializer = serializers.get_serializer("json")
            s = JSONSerializer()
            s.serialize(qSet)
            data = s.getvalue()
            return HttpResponse(content = data)
        except Exception as e:
            data = json.dumps("Error while room filtering")
            return HttpResponse(content = data)
    else:
        data = json.dumps("Unable to filter.")
        return HttpResponse(content = data)