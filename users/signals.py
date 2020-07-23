from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from users.models import User


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if user.id:
        return
    if not user.email:
        return

    try:
        user = User.objects.get(email=user.email)
        sociallogin.connect(request, user)
    except User.DoesNotExist:
        pass
