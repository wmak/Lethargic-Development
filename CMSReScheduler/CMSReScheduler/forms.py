#!/usr/bin/env python
# encoding: utf-8

from django import forms

class UploadCsv(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()