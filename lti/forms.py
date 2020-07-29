from django import forms

from django.contrib.auth.models import User
from account.models import Account

class LtiUsernameForm(forms.Form):
    username = forms.CharField(
        label='Username',
        error_messages={'required': 'The username must be unique'},
        max_length=150
        )
    
    def unique_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return True
        return False
            
    
