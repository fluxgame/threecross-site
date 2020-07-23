from django.db import models


class Item(models.Model):
    RAW = 'RI'
    FINISHED = 'FI'
    MERCH = 'ME'
    NON_INV = 'NI'

    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    type = models.CharField(
        max_length=2,
        choices=[(RAW, 'Raw Materials'), (FINISHED, 'Finished Goods'), (MERCH, 'Merchandise'), (NON_INV, 'Non-Inventory')],
        default=NON_INV
    )

    def __str__(self):
        return self.name
