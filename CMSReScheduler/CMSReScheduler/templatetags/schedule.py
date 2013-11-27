from django import template
from django.utils.safestring import mark_safe
from classes.models import Course, Department, CourseSchedule, Room

register = template.Library()

daysOfWeek = [
["MO", "Monday"],
["TU", "Tuesday"],
["WE", "Wednesday"], 
["TH", "Thursday"],
["FR", "Friday"]
]

@register.filter
def get_range(value):
	return range(value)

@register.filter
def schedule_day(value):
	try:
		return daysOfWeek[value][1]
	except Exception as e:
		return ""

@register.filter
def get_time(value, arg=False):
	if arg:
		if value + 5 > 12:
			return str(value - 7) + ":00 PM"
		else:
			return str(value + 5) + ":00 AM"
	else:
		return str(value + 7) + ":00:00"

@register.filter
def schedule_time(value):
	if value + 5 > 12:
		return str(value - 7) + ":00 PM"
	else:
		return str(value + 5) + ":00 AM"

@register.filter
#def has_course(value, arg):

def get_courses_by_day(value):
	return CourseSchedule.objects.filter(dayOfWeek=daysOfWeek[value][0])

@register.filter
def get_course(value, arg):
	course = value.filter(startTime=arg)
	if not course:
		return None
	else:
		return course[0]

@register.filter
def get_courses_by_day(value):
        return CourseSchedule.objects.filter(dayOfWeek=daysOfWeek[value][0])
