from django import forms
from django.conf import settings
from .models import Member


class MemberCreationForm(forms.models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberCreationForm, self).__init__(*args, **kwargs)
        if settings.TARGET_ENV == "dev":
            self.fields['first_name'].initial = 'Dave'
            self.fields['last_name'].initial = 'Howland'
            self.fields['birth_date'].initial = '10/21/1981'

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'birth_date')
