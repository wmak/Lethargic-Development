#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.forms import ModelForm
from classes.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UploadCsv(forms.Form):
	title = forms.CharField(max_length=100)
	file = forms.FileField()

class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
	newpassword = forms.CharField(max_length=20, widget=forms.PasswordInput())
	newpassword2= forms.CharField(max_length=20, widget=forms.PasswordInput())

class ProfileEditForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user']

class UserEditForm(ModelForm):
	class Meta:
		model = User
		exclude = ['username', 'password1']
		fields = ['first_name', 'last_name', 'email']

class AdminUserEditForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']

class RegisterForm(UserCreationForm):
	email = forms.EmailField(label = "Email address")
	first_name = forms.CharField(label = "Name")
	last_name = forms.CharField(label = "Surname")

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None
 
	# this sets the order of the fields
	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "username", "password1", "password2", )
 
	# this redefines the save function to include the fields you added
	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
 
		if commit:
			user.save()
		return user
