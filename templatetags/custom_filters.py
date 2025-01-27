# your_app/templatetags/custom_filters.py
from django import template
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def custom_date_format(value, date_format):
    if value:
        local_dt = localtime(value)
        return local_dt.strftime(date_format)
    return value

