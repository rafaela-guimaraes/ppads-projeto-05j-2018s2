from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def format_currency_symbol(value):
    if value is None:
        value = 0
    value = round(float(value), 2)
    return "R$%s%s" % (intcomma(int(value)), ("%0.2f" % value)[-3:])
        

@register.filter
def format_currency(value):
    if value is None:
        value = 0
    value = round(float(value), 2)
    return "%s%s" % (intcomma(int(value)), ("%0.2f" % value)[-3:])
