from django.urls import path

from . import views


urlpatterns = [
    path("", views.VocabularyListListView.as_view(), name="vocab_list_list"),
    path("<int:pk>/", views.VocabularyListDetailView.as_view(), name="vocab_list_detail"),
]