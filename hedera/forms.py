from django import forms

from account.forms import SettingsForm as AccountSettingsForm
from account.forms import SignupForm as AccountSignupForm


class SettingsForm(AccountSettingsForm):

    display_name = forms.CharField(max_length=250, required=False)

    field_order = ["display_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["timezone"]
        del self.fields["language"]


class SignupForm(AccountSignupForm):

    display_name = forms.CharField(max_length=250)

    field_order = ["display_name", "email", "password", "password_confirm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["username"]
