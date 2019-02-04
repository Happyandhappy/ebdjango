from django import template

register = template.Library()

@register.filter
def eli_brackets(value):
    return value.replace('[', '').replace(']', '').replace("'", '')


