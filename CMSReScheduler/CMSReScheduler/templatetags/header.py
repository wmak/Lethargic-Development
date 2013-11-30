from django import template
from classes.models import UserProfile

register = template.Library()

@register.filter
def count(value):
	return value.count()

@register.filter
def is_admin(value):
	user = UserProfile.objects.get(user=value)
	return user.role == "admin"