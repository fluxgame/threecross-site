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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from surveys import views as survey_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('apply', user_views.apply_view, name='apply'),
    path('members/password/change/', user_views.login_after_password_change, name='account_change_password'),
    path('members/', user_views.profile_view, name='profile'),
    path('members/', include('allauth.urls')),
    path('members/surveys/<slug:slug>,<int:id>', survey_views.survey_view, name="survey"),
    path('ajax/survey_vote', survey_views.ajax_vote_view, name="survey_vote"),
    path('members/nominate_charity', survey_views.nominate_charity_view, name="nominate_charity")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
