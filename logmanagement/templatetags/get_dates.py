__author__ = 'charls'
from django import template
import datetime
register = template.Library()


@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    #timezone = context['timezone']
    return datetime.datetime.now().strftime(format_string)