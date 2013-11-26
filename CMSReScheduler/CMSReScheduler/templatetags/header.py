from django import template
from classes.models import UserProfile

register = template.Library()

@register.filter
def count(value):
	return value.count()