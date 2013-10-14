from django.db import models

# Create your models here.

class Course(models.Model):
	code = models.CharField(max_length=9) #ex. CSCC01H3F
	enrolment = models.IntegerField()