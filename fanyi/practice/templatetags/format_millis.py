from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_millis(ms):
    td = timedelta(milliseconds=ms)
    td = timedelta(days=td.days, seconds=td.seconds)
    return str(td)
