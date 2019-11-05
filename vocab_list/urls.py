from django.urls import path

from . import views


urlpatterns = [
    path("", views.VocabularyListListView.as_view(), name="vocab_list_list"),
    path("create/", views.VocabularyListCreateView.as_view(), name="vocab_list_create"),
    path("<int:pk>/", views.VocabularyListDetailView.as_view(), name="vocab_list_detail"),
    path("personal/create/", views.PersonalVocabularyListEntriesCreateView.as_view(), name="vocab_list_personal_create"),
    path("personal/<str:lang>/", views.PersonalVocabListDetailView.as_view(), name="vocab_list_personal_detail"),
]
