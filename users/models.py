from cuser.models import CUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import Group as BaseGroup
import uuid


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(
        "Email Address",
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    def is_member(self):
        return self.member is not None

    @property
    def full_name(self):
        try:
            return self.business.name
        except:
            try:
                return self.member.full_name
            except:
                pass

        return self.email

    @property
    def sort_name(self):
        try:
            return self.business.sort_name
        except:
            try:
                return self.member.sort_name
            except:
                pass

        return self.email

    @property
    def street_address(self):
        try:
            return self.address.street
        except:
            return 'N/A'

    @property
    def city_state(self):
        try:
            return self.address.city, self.address.state
        except:
            return 'N/A'

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Group(BaseGroup):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True


@receiver(pre_save, sender=get_user_model())
def random_email(sender, instance, **kwargs):
    if not instance.email:
        instance.email = uuid.uuid4().hex[:30] + '@3cross.coop'


@receiver(pre_save, sender=get_user_model())
def validate_either_member_or_business(sender, instance, **kwargs):
    try:
        if instance.member and instance.business:
            raise ValidationError("User cannot be both a member and a business.")
    except:
        pass
