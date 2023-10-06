from django import template
register = template.Library()


@register.filter
def is_active(mobject):
    results = mobject.filter(is_active=True)
    return set(results)
