from django import template

register = template.Library()


@register.filter
def split_string(value, delimiter):
    unique_parts = sorted(set(part.strip() for part in value.split(delimiter)))
    return unique_parts
