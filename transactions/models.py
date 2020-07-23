from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from items.models import Item


class Transaction(models.Model):
    BUY = 'BU'
    SELL = 'SE'
    USE = 'US'
    PACKAGE = 'PA'

    date = models.DateTimeField(null=False)
    action = models.CharField(
        max_length=2,
        choices=[(BUY, 'Buy'), (SELL, 'Sell'), (USE, 'Use'), (PACKAGE, 'Package')],
        default=SELL
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qty = models.IntegerField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.date)
