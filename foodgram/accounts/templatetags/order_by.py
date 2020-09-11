from django import template

register = template.Library()


@register.filter
def order_by(queryset, field):
    return queryset.order_by(field)
