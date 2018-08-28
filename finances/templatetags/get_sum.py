from django import template
register = template.Library()

@register.filter
def get_sum(List, i):
    return List[int(i)].get('amount__sum')

@register.filter
def get_balance(income, expense):
    if income == None or expense == None:
        return 0
    else:
        return income - expense