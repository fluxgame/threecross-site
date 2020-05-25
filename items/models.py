from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
