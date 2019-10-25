from django import forms
from django.conf import settings

from .models import VocabularyList


class VocabularyListForm(forms.ModelForm):

    lang = forms.ChoiceField(label="Language", choices=settings.SUPPORTED_LANGUAGES)
    data = forms.FileField(label="Vocabulary Entries", help_text="Expects a TAB delimited file as exported from Excel or Google Sheets")

    class Meta:
        model = VocabularyList
        fields = ["title", "description", "lang", "data"]
