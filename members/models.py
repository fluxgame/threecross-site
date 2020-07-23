from datetime import datetime

from django.db import models
from django.db.models import Sum

from businesses.models import Business
from items.models import Item
from transactions.models import Transaction
from django.contrib.auth.models import User
from django.conf import settings
from addresses.models import Address


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField("First Name", max_length=256)
    last_name = models.CharField("Last Name", max_length=256)
    number = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField("Birth Date", null=True, blank=True)
    card_printed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sort_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def sort_name(self):
        return self.last_name + ', ' + self.first_name

    COMMON = 'Coop Membership'
    PREFERRED = 'Preferred Share'
    QWNA = 'Qualified Written Notice of Allocation'

    @property
    def common_share(self):
        return self.user.transaction_set\
            .filter(item=Item.objects.get(name=Member.COMMON)).first()

    @property
    def ica_balance(self):
        return self.user.transaction_set\
            .filter(item__in=Item.objects.filter(name__in=[Member.COMMON, Member.QWNA]))\
            .aggregate(t=Sum('amount'))['t']

    @property
    def preferred_share_count(self):
        return self.user.transaction_set\
            .filter(item=Item.objects.filter(name=Member.PREFERRED).first())\
            .aggregate(t=Sum('qty'))['t']

    @property
    def preferred_share_value(self):
        return self.user.transaction_set\
            .filter(item=Item.objects.filter(name=Member.PREFERRED).first())\
            .aggregate(t=Sum('amount'))['t']

    @property
    def annual_purchases(self, year=datetime.today().year):
        return self.user.transaction_set\
            .filter(date__year=year)\
            .exclude(item__in=Item.objects.filter(name__in=[Member.COMMON, Member.QWNA, Member.PREFERRED]))\
            .aggregate(t=Sum('amount'))['t']
