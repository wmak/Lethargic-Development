import utils.csvutils as csvutils
from django.shortcuts import render
from classes.models import Course

def home(request):
	return render(request, 'test.html')
