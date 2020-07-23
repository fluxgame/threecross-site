from django import forms
from django.conf import settings
from .models import Address


class AddressCreationForm(forms.models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressCreationForm, self).__init__(*args, **kwargs)

        if settings.TARGET_ENV == "dev":
            self.fields['street'].initial = '45 Havelock Rd'
            self.fields['city'].initial = 'Worcester'
            self.fields['state'].initial = 'MA'
            self.fields['postal_code'].initial = '01602'
            self.fields['phone_number'].initial = '5085564236'

    class Meta:
        model = Address
        fields = ('street', 'unit', 'city', 'state', 'postal_code', 'phone_number')
