from django import template


register = template.Library()


@register.simple_tag
def default_vocab_list(user):
    return user.personalvocabularylist_set.all().order_by("lang").first()
