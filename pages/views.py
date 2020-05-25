from django.shortcuts import render

from .models import Question
from accounts.models import Account

# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "home.html", {"name": "home"})


def about_view(request, *args, **kwargs):
    return render(request, "about.html", {"name": "about"})


def cooperate_view(request, *args, **kwargs):
    return render(request, "cooperate.html", {"name": "cooperate"})


def visit_view(request, *args, **kwargs):
    return render(request, "visit.html", {"name": "visit"})


def find_view(request, *args, **kwargs):
    on_accounts = sorted(
        Account.objects.filter(show_on_web=True).filter(type=Account.ON),
        key=lambda t: t.sort_name,
        reverse=False
    )
    off_accounts = sorted(
        Account.objects.filter(show_on_web=True).filter(type=Account.OFF),
        key=lambda t: t.sort_name,
        reverse=False
    )

    return render(request, "find.html", {
        "name": "find our beer",
        "id": "find",
        "on_accounts": on_accounts,
        "off_accounts": off_accounts
    })


def sustainability_view(request, *args, **kwargs):
    return render(request, "sustainability.html", {"name": "sustainability"})


def faq_view(request, *args, **kwargs):
    return render(request, "faq.html", {
        "name": "faq",
        "faqs": Question.objects.all().order_by('sort_order')
    })


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {"name": "contact"})
