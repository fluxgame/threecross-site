from django.db import models

# Create your models here.


class Account(models.Model):
    ON = 'ON'
    OFF = 'OF'
    DIST = 'DI'

    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    website = models.URLField(blank=True)
    type = models.CharField(
        max_length=2,
        choices=[(ON, 'On-Premise'), (OFF, 'Off-Premise'), (DIST, 'Distributor')],
        default=OFF
    )
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    show_on_web = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def sort_name(self):
        name = self.name

        starts_with_flags = [
            'the ',
            'an ',
            'a '
        ]

        for flag in starts_with_flags:
            if name.lower().startswith(flag):
                return "%s, %s" % (name[len(flag):], name[:len(flag)-1])
            else:
                pass
        return self.name
