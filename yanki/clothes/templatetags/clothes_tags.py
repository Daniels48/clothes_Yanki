from django import template
from clothes.models import *

register = template.Library()


@register.simple_tag()
def get_tags():
    return Tag.objects.all()


@register.simple_tag()
def get_size():
    return Size.objects.all()


@register.simple_tag()
def get_color():
    return Color.objects.all()


@register.simple_tag()
def get_category():
    return Catalog.objects.all()


@register.inclusion_tag('clothes/breadcrumb.html', name="crumb")
def catalog_breadcrumb(category):
    return {'category': category}
