__author__ = 'charls'

from django import template
import datetime
from logmanagement.parser.InputsHandler import InputsHandler
register = template.Library()


@register.simple_tag(takes_context=True)
def get_logs(context):
    file_handler = InputsHandler()
    return file_handler.get_file_contents(context['folder'],context['log_file'])

@register.simple_tag(takes_context=True)
def get_key(context,key):
    return context.get(key)
