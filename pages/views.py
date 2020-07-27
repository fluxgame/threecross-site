import datetime

from django.shortcuts import render, redirect
from django.views.generic.base import View

from threecross_site import settings
from .models import Question, Announcement
from users.models import User


class PageView(View):

    class Meta:
        page_name = None
        path = None
        verbose = None
        navbar = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.Meta.page_name is None:
            raise NotImplemented

    def get_kwargs(self, **kwargs):
        return {
            'verbose': self.Meta.verbose,
            # 'navbar': self.Meta.navbar,
            **kwargs
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.Meta.page_name + ".html", {**self.get_kwargs(**kwargs)})


class HomeView(PageView):

    def get_kwargs(self, **kwargs):
        return {
            **super().get_kwargs(**kwargs),
            'announcements': Announcement.objects.filter(
                start_date__lt=datetime.date.today(),
                end_date__gt=datetime.date.today()).order_by('start_date').all()
            }

    class Meta:
        page_name = verbose = 'home'
        path = ''


def get_accounts(group_name):
    return sorted(
        User.objects.filter(is_active=True).filter(groups__name=group_name),
        key=lambda t: t.sort_name,
        reverse=False)


class FindView(PageView):

    def get_kwargs(self, **kwargs):
        return {
            **super().get_kwargs(**kwargs),
            'on_accounts': get_accounts("On-Premise Retail"),
            'off_accounts': get_accounts("Off-Premise Retail")
        }

    class Meta:
        page_name = path = 'find'
        verbose = 'find our beer'


class VisitView(PageView):

    def get_kwargs(self, **kwargs):
        return {
            **super().get_kwargs(**kwargs),
            'google_api_key': settings.GOOGLE_API_KEY
        }

    class Meta:
        page_name = path = verbose = 'visit'


class FaqView(PageView):

    def get_kwargs(self, **kwargs):
        return {
            **super().get_kwargs(**kwargs),
            "faqs": Question.objects.all().order_by('sort_order')
        }

    class Meta:
        path = page_name = verbose = 'faq'


class ShopView(View):

    def get(self, request, *args, **kwargs):
        return redirect("https://biermi.com/store/3crossfermentation/store")

    class Meta:
        path = page_name = verbose = 'shop'


class AboutView(PageView):
    class Meta:
        path = page_name = verbose = 'about'


class CooperateView(PageView):
    class Meta:
        path = page_name = verbose = 'cooperate'


class SustainabilityView(PageView):
    class Meta:
        path = page_name = verbose = 'sustainability'


class ContactView(PageView):
    class Meta:
        path = page_name = verbose = 'contact'


class ProfileView(PageView):
    class Meta:
        path = page_name = verbose = 'profile'


pages = [HomeView, AboutView, CooperateView, VisitView, FindView, SustainabilityView, FaqView, ShopView, ContactView]
