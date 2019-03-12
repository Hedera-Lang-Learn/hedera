from django.urls import path

from . import views


urlpatterns = [
    path("<int:node_id>.json", views.node_json, name="node_json"),
]
