from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street = models.CharField('Street Address', max_length=256, blank=False)
    unit = models.CharField('Unit #', max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=False)
    state = models.CharField(max_length=2, blank=False)
    postal_code = models.CharField('Postal Code', max_length=10, blank=False)
    phone_number = PhoneNumberField('Phone Number')
