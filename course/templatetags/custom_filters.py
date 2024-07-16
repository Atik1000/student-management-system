# course/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def getattr_custom(obj, attr_name):
    return getattr(obj, attr_name, None)
