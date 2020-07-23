from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.TextField()
    answer = models.TextField()
    sort_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text
