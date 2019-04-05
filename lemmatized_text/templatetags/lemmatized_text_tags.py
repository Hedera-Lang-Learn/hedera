from django import template
from django.template.defaultfilters import floatformat


register = template.Library()


def to_percent(val):
    return floatformat(val * 100, 2) + "%"


@register.simple_tag
def stats_for_text(text, user):
    stats = text.personalvocabularystats_set.filter(vocab_list__user=user).first()
    if stats:
        return {
            "unranked": to_percent(stats.unranked),
            "one": to_percent(stats.one),
            "two": to_percent(stats.two),
            "three": to_percent(stats.three),
            "four": to_percent(stats.four),
            "five": to_percent(stats.five),
        }
