import utils.csvutils as csvutils
from django.shortcuts import render
from classes.models import Course

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from forms import UploadCsv

#from ... import CSVParserFunction

def home(request):
	return render(request, 'test.html')

def csvimport(request):
    if request.method == 'POST':
        form = UploadCsv(request.POST, request.FILES)    
        #csv_parser(request.FILES['file'])
        print(request.FILES['file'])
        #return HttpResponseRedirect('/sucess...')
        return HttpResponse('CSV file imported sucessfully.')
    else:
        form = UploadCsv()
    return render_to_response('csvimport.html', {'form': form}, context_instance=RequestContext(request))
