from __future__ import unicode_literals
from django import template

register = template.Library()

@register.simple_tag
def host():
    return "http://127.0.0.1:8000/"