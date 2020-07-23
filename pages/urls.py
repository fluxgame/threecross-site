from django.urls import path
from . import views

urlpatterns = [path('', views.page_view, name='home')]

for page_name, page_info in views.page_list.items():
    if not page_info['external']:
        urlpatterns.append(path(page_name, page_info['view'], name=page_name))
