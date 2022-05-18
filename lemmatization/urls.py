from django.urls import path

from . import views


urlpatterns = [
    path("<int:lemma_id>.json", views.lemma_json, name="lemma_json"),
]
