from django import forms
from django.conf import settings

from .models import VocabularyList


class VocabularyListForm(forms.ModelForm):

    lang = forms.ChoiceField(label="Language", choices=settings.SUPPORTED_LANGUAGES)
    data = forms.FileField(label="Vocabulary Entries", help_text="Expects a TAB delimited file as exported from Excel or Google Sheets")

    class Meta:
        model = VocabularyList
        fields = ["title", "description", "lang", "data"]


RATINGS = [
    (1, "I don't recognize these words"),
    (2, "I recognize these words but don't know what they mean"),
    (3, "I think I know what these words mean"),
    (4, "I definitely know what these words mean but could forget soon"),
    (5, "I know these words so well, I am unlikely to ever forget them"),
]


class PersonalVocabularyListForm(forms.ModelForm):

    lang = forms.ChoiceField(label="Language", choices=settings.SUPPORTED_LANGUAGES)
    data = forms.FileField(label="Vocabulary Entries", help_text="Expects a TAB delimited file as exported from Excel or Google Sheets")
    rating = forms.ChoiceField(label="Familiarity", choices=RATINGS)

    class Meta:
        model = VocabularyList
        fields = ["lang", "rating", "data"]
