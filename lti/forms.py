from django import forms

from django.contrib.auth import get_user_model


class LtiUsernameForm(forms.Form):
    username = forms.CharField(
        label="Username",
        error_messages={"required": "The username must be unique"},
        max_length=150
    )

    def unique_username(self, username):
        return not get_user_model().objects.filter(username__iexact=username.strip()).exists()