from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AuthUserForm(AuthenticationForm):
    remember_me = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.CheckboxInput(
            attrs={'value': 'keep'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Password',
                'autofocus':True,
                'type': 'password'
            }
        )
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Username or email'
            }
        )