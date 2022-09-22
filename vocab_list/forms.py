from base64 import b64encode

from django import forms

from hedera.supported_languages import SUPPORTED_LANGUAGES

from .models import VocabularyList


LANGUAGES = [[lang.code, lang.verbose_name] for lang in SUPPORTED_LANGUAGES.values()]
RATINGS = [
    (1, "I don't recognize these words"),
    (2, "I recognize these words but don't know what they mean"),
    (3, "I think I know what these words mean"),
    (4, "I definitely know what these words mean but could forget soon"),
    (5, "I know these words so well, I am unlikely to ever forget them"),
]

sampledata = b64encode((
    b"headword\tdefinition\tfamiliarity\n"
    b"your headword\tyour definition\tfamiliarity rating from 1 (least familiar) to 5 (most familiar)"
)).decode('utf-8')

upload_help_text = (
    "Expects a TAB delimited file as exported from Excel or Google Sheets."
    f"</br><a href=\"data:text/csv;base64,{sampledata}\" download=\"vocab_list_template.tsv\">Download a template file</a>"
)


class VocabularyListForm(forms.ModelForm):

    lang = forms.ChoiceField(label="Language", choices=LANGUAGES)
    data = forms.FileField(label="Vocabulary Entries", help_text=upload_help_text)

    class Meta:
        model = VocabularyList
        fields = ["title", "description", "lang", "data"]


class PersonalVocabularyListForm(forms.ModelForm):

    lang = forms.ChoiceField(label="Language", choices=LANGUAGES)
    data = forms.FileField(label="Vocabulary Entries", help_text=upload_help_text)
    rating = forms.ChoiceField(label="Familiarity", choices=RATINGS)

    class Meta:
        model = VocabularyList
        fields = ["lang", "rating", "data"]
