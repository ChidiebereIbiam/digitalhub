
from django.template import Library

register = Library()

@register.filter
def format_image_url(counter):
    return f"images/assets/{counter:02d}.png"