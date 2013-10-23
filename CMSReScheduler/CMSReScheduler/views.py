import utils.csvutils as csvutils
from django.shortcuts import render
from classes.models import Course

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from forms import UploadCsv

def home(request):
	return render(request, 'test.html')


def import_csv_file(request, type):
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

def instructor_schedule(request, name):
    return render_to_request('schedule.html',)



