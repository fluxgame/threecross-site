from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from addresses.models import Address


class Business(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=256)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user_id is None:
            u = get_user_model()()
            u.save()
            self.user_id = u.id
        super(Business, self).save(*args, **kwargs)

    def is_active(instance):
        try:
            return instance.user.is_active
        except:
            return True

    @property
    def full_name(instance):
        return instance.name

    @property
    def sort_name(instance):
        starts_with_flags = [
            'the ',
            'an ',
            'a '
        ]

        for flag in starts_with_flags:
            if instance.name.lower().startswith(flag):
                return "%s, %s" % (instance.name[len(flag):], instance.name[:len(flag)-1])
            else:
                pass
        return instance.name

