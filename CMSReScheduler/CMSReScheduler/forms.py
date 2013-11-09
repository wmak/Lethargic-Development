#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.forms import ModelForm
from classes.models import User

class UploadCsv(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()
