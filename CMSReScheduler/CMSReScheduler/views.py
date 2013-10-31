import utils.csvutils as csvutils
from django.shortcuts import render
from classes.models import Course

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from forms import UploadCsv
from forms import InstructorRegistrationForm

def home(request):
	return render(request, 'test.html')


def import_csv_file(request, type):
    ''' NOTE: for now I have a single url for this. I can send them  each to a certain page if you guys prefer.
    This is still very much up for debate. Let me know what you all think '''
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

def registration(request, type):
    if request.method == 'POST':
        if type == 'instructor':
            form = InstructorRegistrationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return HttpResponse('User registered successfully.')
    else:
        form = InstructorRegistrationForm()
    return render_to_response('registration.html', {'form': form}, context_instance=RequestContext(request))

def instructor_schedule(request, instructor):
    i = Instructor.objects.get(name=instructor)
    context = {"courses": i.myCourses, 'instructor': i.name}
    return render_to_respose('instructor_schedule.html', context, context_instance-RequestContext(request))
