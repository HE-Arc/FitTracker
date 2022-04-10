from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)