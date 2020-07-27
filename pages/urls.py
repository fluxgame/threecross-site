from django.urls import path
from . import views

urlpatterns = []

for view_class in views.pages:
    urlpatterns.append(path(view_class.Meta.path, view_class.as_view(), name=view_class.Meta.page_name))
