import requests
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation

from users.fields import ReCaptchaField
from users.models import User


class UserAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    captcha = ReCaptchaField()


class SimpleUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SimpleUserCreationForm, self).__init__(*args, **kwargs)
        if settings.TARGET_ENV == "dev":
            self.fields['email'].initial = 'fluxgame@gmail.com'
            self.fields['password1'].initial = 'tes1234'

    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        label="Desired Password",
    )
    password2 = None
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('email', 'password1')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password1', error)
        return password1

