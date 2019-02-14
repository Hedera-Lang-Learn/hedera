
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.contrib import admin

from . import views


urlpatterns = [
    path("<int:text_id>/", views.read, name="read"),
]
