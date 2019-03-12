
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.contrib import admin

from . import views


urlpatterns = [
    path("", views.lemmatized_texts, name="lemmatized_texts_list"),
    path("<int:pk>/", views.text, name="lemmatized_texts_detail"),
    path("<int:pk>/learner/", views.learner_text, name="lemmatized_texts_learner"),
    path("<int:pk>/delete/", views.delete, name="lemmatized_texts_delete"),
    path("create/", views.create, name="lemmatized_texts_create"),
]
