from django import template

register = template.Library()
register_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag


@register_tag
def inspect(match, obj=None, target=None):
    """Converts a string into all lowercase"""
    return {'groups': match.groups,
            }
