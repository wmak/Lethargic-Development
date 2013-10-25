import utils.csvutils as csvutils
from django.shortcuts import render
from classes.models import Course

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from forms import UploadCsv
from forms import UserRegistrationForm

def home(request):
	return render(request, 'test.html')

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

def user_registration(request):
    if request.method == 'POST':
        userform = UserRegistrationForm(request.POST)
        if userform.is_valid():
            new_user = userform.save()
            return HttpResponse('User registered successfully.')
        else:
            userform = RegistrationForm()
    return render_to_response('userregistration.html', {'form': userform}, context_instance=RequestContext(request))
