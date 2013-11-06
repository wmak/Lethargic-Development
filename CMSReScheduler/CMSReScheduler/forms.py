#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.forms import ModelForm
from classes.models import User
from classes.models import Instructor

class UploadCsv(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class InstructorRegistrationForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Instructor
		fields =['name', 'address', 'email', 'department', 'room', 'myCourses']
