from django import template

from cms.models import FlatPage, HomePage


register = template.Library()


@register.simple_tag
def get_home_page():
    return HomePage.objects.first()


@register.simple_tag
def get_site_nav():
    return FlatPage.objects.live().filter(show_in_menus=True).order_by('title')


@register.simple_tag
def get_flatpage_nav():
    return HomePage.objects.first().get_children().live().order_by('title')


@register.simple_tag()
def get_flatpage_subnav(page):
    return page.get_children().live().order_by('title')
