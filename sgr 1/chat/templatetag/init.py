from django import template
register = template.Library()

def make_str(value):
    return str(value)
