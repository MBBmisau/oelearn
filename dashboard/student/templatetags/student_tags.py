from django import template

register = template.Library()


@register.filter
def serialize(string):
    my_str = string.title()
    result = my_str.replace('_',' ')
    return result