from django.urls import path

from . import views


urlpatterns = [
    path("", views.GroupListView.as_view(), name="groups_list"),
    path("create/", views.GroupCreateView.as_view(), name="groups_create"),
    path("<slug:slug>/", views.GroupDetailView.as_view(), name="groups_detail"),
    path("<slug:slug>/join/", views.GroupJoinView.as_view(), name="groups_join"),
    path("<slug:slug>/update/", views.GroupUpdateView.as_view(), name="groups_update"),
]
