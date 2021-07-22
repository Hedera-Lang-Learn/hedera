from django import forms

from ckeditor.widgets import CKEditorWidget


class LemmatizedTextEditForm(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(config_name="hedera_ckeditor"))

    def __init__(self, *args, **kwargs):
        self.text_data = kwargs.pop("text_data")
        super().__init__(*args, **kwargs)
        # print(self.text_data)
        # print(self.transform_data_to_html(self.text_data))
        self.fields["text"].initial = self.transform_data_to_html(self.text_data)

    def transform_data_to_html(self, data):
        return "".join([f"{token['word']}{token['following']}" for token in data])
