from django import forms

from ckeditor.widgets import CKEditorWidget


class LemmatizedTextEditForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=CKEditorWidget(config_name="hedera_ckeditor"))
