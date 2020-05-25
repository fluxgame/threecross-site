from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
