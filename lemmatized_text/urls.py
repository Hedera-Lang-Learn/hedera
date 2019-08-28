
from django.urls import path

from . import views


urlpatterns = [
    path("", views.lemmatized_texts, name="lemmatized_texts_list"),
    path("<int:pk>/", views.text, name="lemmatized_texts_detail"),
    path("<int:pk>/learner/", views.learner_text, name="lemmatized_texts_learner"),
    path("<int:pk>/delete/", views.delete, name="lemmatized_texts_delete"),
    path("<int:pk>/retry/", views.retry_lemmatization, name="lemmatized_texts_retry_lemmatization"),
    path("<int:pk>/cancel/", views.cancel_lemmatization, name="lemmatized_texts_cancel_lemmatization"),
    path("create/", views.create, name="lemmatized_texts_create"),
]
