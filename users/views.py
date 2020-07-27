from allauth.account.views import PasswordChangeView
from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from addresses.forms import AddressCreationForm
from members.forms import MemberCreationForm
from pages.utils import slack_notify
from surveys.forms import SurveyResponseForm
from surveys.models import Survey
from users.forms import SimpleUserCreationForm, UserAuthenticationForm
from django.contrib.auth.models import Group
from pages.views import pages


class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('profile')


login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())


@login_required
def profile_view(request, *args, **kwargs):
    if request.user.is_member():
        surveys = Survey.objects.all()
        return render(request, "profile.html", {'surveys': surveys})
    else:
        return redirect('home')


class UserLogoutView(LogoutView):
    next_page = 'home'


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = UserAuthenticationForm
    next = 'profile'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context.update({'recaptcha': True})
        return context


def apply_view(request, *args, **kwargs):
    application_survey = Survey.objects.get(title='Membership Application Questions')

    if request.method == "POST":
        user_form = SimpleUserCreationForm(request.POST)
        member_form = MemberCreationForm(request.POST)
        address_form = AddressCreationForm(request.POST)
        survey_form = SurveyResponseForm(request.POST, survey=application_survey, user=None)
        if user_form.is_valid():
            user = user_form.save()

            survey_form = SurveyResponseForm(request.POST, survey=application_survey, user=user)

            member_form.instance.user = user
            address_form.instance.user = user

            if member_form.is_valid() and address_form.is_valid() and survey_form.is_valid():
                members_group = Group.objects.get(name='Pending Applications')
                members_group.user_set.add(user)
                members_group.save()
                member_form.save()
                address_form.save()
                survey_form.save()

                slack_notify("Membership application received from " + user.full_name +
                             ". reCaptcha score: " + str(user_form.fields['captcha'].score))

                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile')
            else:
                user.delete()
    else:
        user_form = SimpleUserCreationForm()
        member_form = MemberCreationForm()
        address_form = AddressCreationForm()
        survey_form = SurveyResponseForm(survey=application_survey, user=None)

    return render(request, "apply.html", {
        "name": "apply",
        "recaptcha": True,
        'user_form': user_form,
        'member_form': member_form,
        'address_form': address_form,
        'survey_form': survey_form,
    })

