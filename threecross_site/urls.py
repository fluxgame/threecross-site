"""threecross URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from pages.views import home_view, faq_view, find_view, about_view, \
    contact_view, cooperate_view, sustainability_view, visit_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('faq', faq_view),
    path('find', find_view),
    path('about', about_view),
    path('contact', contact_view),
    path('cooperate', cooperate_view),
    path('sustainability', sustainability_view),
    path('visit', visit_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
