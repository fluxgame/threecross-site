from django.shortcuts import render, redirect
from .models import Question
from users.models import User


def page_view(request, *args, **kwargs):
    page_name = request.resolver_match.url_name
    page_info = page_list[page_name] if page_name in page_list else {}

    return render(request, page_name + ".html", {'page_list': page_list, **kwargs, **page_info})


def shop_view(request, *args, **kwargs):
    return redirect("https://biermi.com/store/3crossfermentation/store")


page_list = {
    'about': {},
    'cooperate': {},
    'visit': {},
    'find': {
        'verbose': 'find our beer',
        "on_accounts": sorted(
            User.objects.filter(is_active=True).filter(groups__name="On-Premise Retail"),
            key=lambda t: t.sort_name,
            reverse=False),
        "off_accounts": sorted(
            User.objects.filter(is_active=True).filter(groups__name="Off-Premise Retail"),
            key=lambda t: t.sort_name,
            reverse=False),
    },
    'sustainability': {},
    'faq': {"faqs": Question.objects.all().order_by('sort_order')},
    'shop': {'view': shop_view},
    'contact': {},
    'profile': {'verbose': "members' portal", 'external': True},
}

for page_name, page_info in page_list.items():
    if 'verbose' not in page_info:
        page_info['verbose'] = page_name
    if 'view' not in page_info:
        page_info['view'] = page_view
    if 'navbar' not in page_info:
        page_info['navbar'] = True
    if 'external' not in page_info:
        page_info['external'] = False
