from django import template
register = template.Library()


@register.filter
def is_active(mobject):
    results = mobject.filter(is_active=True)
    return set(results)


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)
