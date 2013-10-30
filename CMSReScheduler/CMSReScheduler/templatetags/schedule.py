from django import template

register = template.Library()

@register.filter
def get_range(value):
	return range(value)

@register.filter
def schedule_cell_day(value):
	if value == 1:
		return "schedule-day"
	else:
		return ""

@register.filter
def schedule_day(value):
	# TODO: Refactor
	if value == 1:
		return "Monday"
	elif value == 2:
		return "Tuesday"
	elif value == 3:
		return "Wednesday"
	elif value == 4:
		return "Thursday"
	elif value == 5:
		return "Friday"
	else:
		return ""

@register.filter
def schedule_cell_time(value):
	if value == 1:
		return "schedule-time"
	else:
		return ""

@register.filter
def schedule_time(value):
	if value + 5 > 12:
		return str(value - 7) + ":00 PM"
	else:
		return str(value + 5) + ":00 AM"
